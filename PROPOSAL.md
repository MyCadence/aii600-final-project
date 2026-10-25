# Proposal

## Hypothesis

For a weekly Saturday 7–9 p.m. outdoor yoga class in Fairfax, a Friday evening NOAA forecast can support you, the organizer, to choose whether to rent a canopy. Estimate the probability using the CoCoRaHS 24 hour precipitation report that covers Saturday's records of measurable rain (at least 0.01 in). The forecast quantity is the probability, in percent, for the report ending Sunday morning.

## Data

The observed outcome will come from CoCoRaHS station [VA-FX-121, Fairfax 3.2 W](https://dex.cocorahs.org/stations/VA-FX-121/): 1,551 daily precipitation reports, May 16, 2022–August 23, 2026, with 99% of days covered. These are volunteer rain-gauge reports, generally read in the morning. There are 223 candidate Saturdays in this period before checking missing Saturday reports and matching forecast availability. Forecasts will come from NOAA’s archived [National Blend of Models (NBM) probabilistic text products](https://vlab.noaa.gov/web/mdl/nbm-text-archives). I will verify the issue time and valid window can be matched before modeling. A daily gauge total includes rain outside the 7–9 p.m. class and its reporting window may differ slightly from the forecast window, so it is an imperfect, potentially noisy dataset for class time rain. CoCoRaHS data are released under CC BY 3.0 with attribution. NOAA source terms and attribution will be recorded before deciding whether forecast files can be republished.

## Decision affected by the model

You, as a hypothetical Fairfax yoga organizer, decide Friday evening whether to rent a 10×20 canopy for Saturday class. A local rental listing gives an example price of [$150](https://www.novaeventrentals.com/). A Fairfax studio lists [$27 per class participant](https://www.sunandmoonstudio.com/class-plans), used only as a revenue benchmark. If there are n paid attendees, the simplified loss of cancelling without a canopy is $27 × n. Renting costs $150, before delivery or setup. Rent when (forecast rain probability × $27 × n) is greater than $150. For six or more attendees, missing a rainy day can cost more than the canopy. At five or fewer, renting for a dry day costs more under these assumptions. The decision depends on actual attendance, cancellation policy, and whether the canopy makes class feasible in rain.
