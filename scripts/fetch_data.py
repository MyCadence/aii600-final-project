"""Build matched Fairfax Saturday rain observations and archived NBM forecasts.

Only a small byte range containing the KIAD station bulletin is downloaded from
each NOAA archive object. CoCoRaHS daily CSV exports are fetched one report date
at a time and reduced to VA-FX-121.
"""

from __future__ import annotations

import concurrent.futures
import csv
import datetime as dt
import io
import re
import time
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "matched_saturdays.csv"
STATION = "VA-FX-121"
NBM_STATION = "KIAD"
START_SATURDAY = dt.date(2022, 5, 21)
END_SATURDAY = dt.date(2026, 8, 22)
NBM_CYCLE = 13
USER_AGENT = "AII600-student-project/1.0 (public course project)"
HEADER_RE = re.compile(rb"(?m)^[ \t]*([A-Z0-9]{4,6})[ \t]+NBM V[0-9.]+ NBE GUIDANCE")


def saturdays() -> list[dt.date]:
    day = START_SATURDAY
    while day.weekday() != 5:
        day += dt.timedelta(days=1)
    result = []
    while day <= END_SATURDAY:
        result.append(day)
        day += dt.timedelta(days=7)
    return result


def ranged_get(session: requests.Session, url: str, start: int, end: int) -> tuple[bytes, int | None]:
    response = session.get(
        url,
        headers={"Range": f"bytes={start}-{end}", "User-Agent": USER_AGENT},
        timeout=45,
    )
    response.raise_for_status()
    total = None
    content_range = response.headers.get("Content-Range", "")
    match = re.search(r"/([0-9]+)$", content_range)
    if match:
        total = int(match.group(1))
    if response.status_code == 200 and start > 0:
        # A server that ignores ranges has returned the full object.
        return response.content[start : end + 1], len(response.content)
    return response.content, total


def find_station_header(session: requests.Session, url: str, station: str) -> tuple[int, int]:
    """Binary-search the station-sorted text bulletin using HTTP byte ranges."""
    first, total = ranged_get(session, url, 0, 1023)
    if total is None:
        head = session.head(url, headers={"User-Agent": USER_AGENT}, timeout=45)
        head.raise_for_status()
        total = int(head.headers["Content-Length"])
    low, high = 0, total - 1
    width = 65536
    for _ in range(24):
        middle = (low + high) // 2
        start = max(0, middle - width // 2)
        end = min(total - 1, start + width - 1)
        chunk, _ = ranged_get(session, url, start, end)
        candidates = []
        for item in HEADER_RE.finditer(chunk):
            absolute = start + item.start()
            # The first partial line can begin before the requested interval.
            if absolute >= middle:
                candidates.append((absolute, item.group(1).decode("ascii")))
        if not candidates:
            high = middle - 1
            continue
        position, found_code = candidates[0]
        if found_code == station:
            return position, total
        if found_code < station:
            low = position + 1
        else:
            high = position - 1
    # A generous local scan handles occasional station-order/version changes.
    start = max(0, min(low, total - 2_000_000))
    end = min(total - 1, start + 4_000_000)
    chunk, _ = ranged_get(session, url, start, end)
    for item in HEADER_RE.finditer(chunk):
        if item.group(1).decode("ascii") == station:
            return start + item.start(), total
    raise RuntimeError(f"Could not locate {station} in {url}")


def parse_nbm(session: requests.Session, saturday: dt.date) -> dict[str, object]:
    friday = saturday - dt.timedelta(days=1)
    date_text = friday.strftime("%Y%m%d")
    cycle = f"{NBM_CYCLE:02d}"
    url = (
        "https://noaa-nbm-grib2-pds.s3.amazonaws.com/"
        f"blend.{date_text}/{cycle}/text/blend_nbetx.t{cycle}z"
    )
    header_at, total = find_station_header(session, url, NBM_STATION)
    chunk, _ = ranged_get(session, url, header_at, min(total - 1, header_at + 12000))
    text = chunk.decode("ascii", errors="replace")
    lines = text.splitlines()
    if not lines or not lines[0].lstrip().startswith(NBM_STATION):
        raise RuntimeError(f"Range did not start at the {NBM_STATION} header for {saturday}")
    block_lines = [lines[0]]
    for line in lines[1:]:
        if HEADER_RE.match(line.encode("ascii", errors="ignore")):
            break
        block_lines.append(line)

    def values(tag: str) -> list[int]:
        for line in block_lines:
            label = line.lstrip()[:3]
            if label == tag:
                remainder = line.lstrip()[3:]
                return [int(v) for v in re.findall(r"-?\d+", remainder)]
        raise RuntimeError(f"Missing {tag} row for {NBM_STATION} on {saturday}")

    forecast_hours = values("FHR")
    pop12 = values("P12")[: len(forecast_hours)]
    issued = dt.datetime.combine(friday, dt.time(NBM_CYCLE), tzinfo=dt.timezone.utc)
    valid = [issued + dt.timedelta(hours=h) for h in forecast_hours]
    target_date = saturday + dt.timedelta(days=1)
    wanted = [
        dt.datetime.combine(target_date, dt.time(hour), tzinfo=dt.timezone.utc)
        for hour in (0, 12)
    ]
    indexes = []
    for target in wanted:
        try:
            indexes.append(valid.index(target))
        except ValueError as exc:
            raise RuntimeError(
                f"No 12-hour forecast ending {target.isoformat()} in {url}"
            ) from exc
    if len(pop12) != len(forecast_hours):
        raise RuntimeError(f"P12/FHR length mismatch for {saturday}")
    p_day, p_night = (pop12[i] for i in indexes)
    if not 0 <= p_day <= 100 or not 0 <= p_night <= 100:
        raise RuntimeError(f"Invalid P12 values for {saturday}: {p_day}, {p_night}")
    version_match = re.search(r"NBM (V[0-9.]+) NBE GUIDANCE", lines[0])
    return {
        "nbm_issue_utc": issued.isoformat(),
        "nbm_version": version_match.group(1) if version_match else "unknown",
        "nbm_station": NBM_STATION,
        "p12_ending_00z_sunday_pct": p_day,
        "p12_ending_12z_sunday_pct": p_night,
        "nbm_archive_url": url,
    }


def fetch_observation(session: requests.Session, saturday: dt.date) -> dict[str, object]:
    observation_date = saturday + dt.timedelta(days=1)
    url = "https://data.cocorahs.org/cocorahs/export/exportreports.aspx"
    response = session.get(
        url,
        params={
            "ReportType": "Daily",
            "Format": "CSV",
            "StartDate": observation_date.isoformat(),
            "EndDate": observation_date.isoformat(),
            "State": "VA",
        },
        headers={"User-Agent": USER_AGENT},
        timeout=45,
    )
    response.raise_for_status()
    rows = [
        r
        for r in csv.DictReader(io.StringIO(response.text))
        if r["StationNumber"].strip() == STATION
    ]
    if len(rows) == 0:
        return {
            "observation_date": observation_date.isoformat(),
            "observation_time_local": "missing",
            "precipitation_in": None,
            "rain_0_01in": None,
            "cocorahs_station": STATION,
            "latitude": None,
            "longitude": None,
            "cocorahs_export_url": response.url,
        }
    if len(rows) > 1:
        raise RuntimeError(f"Expected at most one {STATION} report for {observation_date}, found {len(rows)}")
    report = rows[0]
    raw_amount = report["TotalPrecipAmt"].strip()
    amount = 0.0 if raw_amount.upper() in {"T", "TRACE", "NA", ""} else float(raw_amount)
    observation_time = report["ObservationTime"].strip()
    return {
        "observation_date": observation_date.isoformat(),
        "observation_time_local": observation_time,
        "precipitation_in": amount,
        "rain_0_01in": int(amount >= 0.01),
        "cocorahs_station": STATION,
        "latitude": float(report["Latitude"]),
        "longitude": float(report["Longitude"]),
        "cocorahs_export_url": response.url,
    }


def build_one(saturday: dt.date) -> dict[str, object]:
    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})
        observation = fetch_observation(session, saturday)
        forecast = parse_nbm(session, saturday)
    return {"saturday": saturday.isoformat(), **observation, **forecast}


def main() -> None:
    dates = saturdays()
    records: list[dict[str, object]] = []
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        jobs = {pool.submit(build_one, day): day for day in dates}
        for future in concurrent.futures.as_completed(jobs):
            day = jobs[future]
            try:
                records.append(future.result())
            except Exception as exc:  # Keep the failure visible; do not invent rows.
                failures.append(f"{day.isoformat()}: {exc}")
    records.sort(key=lambda r: str(r["saturday"]))
    if len(records) != len(dates):
        message = "\n".join(failures[:20])
        raise RuntimeError(
            f"Matched {len(records)} of {len(dates)} candidate Saturdays. First failures:\n{message}"
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    import pandas as pd

    pd.DataFrame(records).to_csv(OUT, index=False)
    print(f"Wrote {len(records)} matched Saturday records to {OUT}")
    if failures:
        print("Failures:\n" + "\n".join(failures))


if __name__ == "__main__":
    main()
