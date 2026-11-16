# Proposal

## Hypothesis

For a weekly Saturday 7-9 p.m. outdoor yoga class in Fairfax, use a Friday NOAA NBM forecast to estimate the probability that the CoCoRaHS 24-hour report ending Sunday morning records at least 0.01 inches of rain by the Friday 11:59 p.m. canopy decision deadline. The target is the daily report; class hours are the decision setting, not the event window being forecast.

## Data

The outcome is the Sunday-morning daily report from CoCoRaHS station [VA-FX-121, Fairfax 3.2 W](https://dex.cocorahs.org/stations/VA-FX-121/). I matched 222 of 223 candidate Saturdays, May 21, 2022–August 22, 2026; one report is missing. Forecast inputs are the two NOAA [NBM extended-text (NBE) 12-hour precipitation probabilities](https://vlab.noaa.gov/web/mdl/nbm-text-products) ending Sunday 00Z and 12Z, from Friday’s 13Z run. The forecast station, KIAD, is about 14 km from the rain gauge; the report also includes rain outside the 7-9 p.m. class. It is a daily-report target, not a direct class-hour label. CoCoRaHS data are CC BY 4.0 with attribution; NOAA forecast data are public domain.

## Decision affected by the model

The organizer decides by Friday 11:59 p.m. whether to rent a 10×20 canopy for Saturday. A local listing gives an example rental price of [$150](https://www.novaeventrentals.com/); a Fairfax studio’s [$27 class price](https://www.sunandmoonstudio.com/class-plans) is only a gross-revenue proxy. With n paid attendees, the simplified no-canopy loss on a wet daily report is $27 × n, so rent when p × $27 × n > $150. At n=8, missing a wet report costs $216 versus $150 for renting on a dry-report day. Preliminary scores use n=8 (threshold 69.4%) and also show n=6 and n=10. Actual attendance, profit, delivery/setup costs, and whether a canopy makes class feasible in rain remain uncertain.
