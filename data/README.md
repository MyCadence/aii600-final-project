# Data

## Sources and terms

- CoCoRaHS daily precipitation CSV export: [data.cocorahs.org export](https://data.cocorahs.org/cocorahs/export/exportreports.aspx). The source describes its data as CC BY 4.0 unless otherwise noted. We attribute Community Collaborative Rain, Hail & Snow Network (CoCoRaHS) and preserve station/date fields.
- NOAA National Blend of Models (NBM) archived extended-text bulletin (NBE), Friday 13Z cycle: [NOAA AWS archive](https://noaa-nbm-grib2-pds.s3.amazonaws.com/). NOAA forecast products are public domain. The extraction script retrieves only the KIAD station block by HTTP byte range; raw bulletin files are not copied into this repository.

## Rebuild and release

From the repository root, run `python scripts/fetch_data.py`. It downloads only the selected Virginia CoCoRaHS daily exports and the relevant KIAD NBM bulletin byte ranges, then writes the matched CSV below. Python dependencies are pinned in `requirements.txt`.

The notebook reads `data/matched_saturdays.csv`. It is excluded from git; attach it as an asset to the public GitHub release tagged `data` before the checkpoint. After the release is created, download it in a clone with `gh release download data --dir data --repo MyCadence/aii600-final-project`.

## File and integrity

- `matched_saturdays.csv` — one row per candidate Saturday from 2022-05-21 through 2026-08-22. CoCoRaHS outcome is the following Sunday morning report at VA-FX-121; NBM predictors are KIAD 12-hour precipitation probabilities for windows ending Sunday 00Z and 12Z. There are 223 candidate rows and 222 observed reports; the missing outcome remains blank.
- SHA-256: `4BA7F83563670174BE36BDB83035CBC1D0067981F65E8201F75F84CCD231F808`

The NBM airport is about 14 km from the CoCoRaHS gauge. Report windows vary with the volunteer’s reading time; 221 observed records are at 7:00 a.m. local and one is at 7:45 a.m. The resulting daily label is a proxy for Saturday class-time rain, not a direct measurement of rain during the class.
