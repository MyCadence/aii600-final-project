# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## 2026-10-24: Define the Saturday rain-and-canopy decision

* Decision. Study a weekly Saturday 7–9 p.m. outdoor yoga class in Fairfax. Estimate the chance of measurable rain (at least 0.01 in) in the CoCoRaHS daily report covering Saturday, using an archived NOAA NBM probability forecast available Friday evening. Compare renting a 10×20 canopy with holding class without one.
* Why. CoCoRaHS station VA-FX-121 (Fairfax 3.2 W) has daily reports from May 16, 2022 through August 23, 2026, with 99% daily coverage. A local rental listing gives a $150 canopy example; a Fairfax studio’s $27 drop-in price is used only as a benchmark for potentially lost class revenue. The daily gauge period includes hours beyond the class, so it is an imperfect proxy for class-time rain. The simplified break-even rule is forecast rain probability × $27 × paid attendees > $150.
* Alternative. Use hourly rain at a nearby airport to label rain during 7–9 p.m. I set that aside because the selected gauge is in Fairfax and this proposal uses a daily outcome; revisit if daily totals prove too weak a proxy for the decision.
* Revisit. Change the target or data if NOAA’s archive cannot supply forecasts issued before the Friday decision with a usable valid-time match, if Saturday gauge reports are too sparse, or if actual attendance, cancellation, canopy, delivery, or setup costs materially change the loss rule.
