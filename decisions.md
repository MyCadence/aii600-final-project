# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## 2026-10-24: Define the Saturday rain and canopy decision

* Decision. Study a (weekly) Saturday afternoon outdoor yoga class in Fairfax. Estimate the chance of rain (at least 0.01 IN) using the National Oceanic and Atmospheric Administration National Blend of Models (NOAA NBM) by a deadline of Friday 11:59 PM (assume you decide whether to pitch the tents). Use the Community Collaborative Rain, Hail and Snow Network (CoCoRaHS) to verify the outcome of Saturday's rainfall (24 hour period). CoCoRaHS is a non-profit, community network of volunteers that report precipitation in their backyard. Compare renting a 10×20 canopy with holding a yoga class without one.
* Why. CoCoRaHS station VA-FX-121 (Fairfax 3.2 W) has daily reports from May 16, 2022 through August 23, 2026, with close to 100% daily coverage. A local rental listing gives a $150 canopy example. A Fairfax studio’s $27 drop in price is used only as a benchmark for potentially lost revenue. The daily rain measurement period includes hours beyond the class, so it's not an ideal scope for class time rain which would typically span a couple hours at most. The break even rule is (forecast rain probability × $27 × paid attendees) > $150.
* Alternative. Use hourly rain at a nearby airport to label rain during class time (7–9 p.m.). I set that aside because the selected measurement is in Fairfax and this proposal uses a daily outcome. We will revisit that method if daily totals prove too weak a gauge for the decision.
* Revisit. Change the target or data if NOAA’s archive cannot supply forecasts issued before the Friday decision with a usable valid-time match, if Saturday reports are too sparse, or if actual attendance, canopy, delivery, or extra setup costs materially change the loss rule.

## 2026-11-15: Preliminary model and held-out evaluation

* Split. Use Saturdays through 2025-12-27 for training (189 complete reports) and hold out 2026-01-03–2026-08-22 (33 complete reports); keep the 2026-01-18 missing CoCoRaHS outcome blank and exclude it from scoring so later weather never informs fitting.
* Model. Compare the training rain frequency (baseline) with an L2-regularized logistic calibration of Friday 13Z NBM NBE P12 forecasts ending Sunday 00Z and 12Z; set this two-input form before scoring 2026, and revisit it if forecast calibration or the airport-to-gauge mismatch changes the decision.
* Loss. Use $150 canopy rental versus $27 × n gross revenue at risk on a wet report, rent when p × $27 × n > $150, score first at illustrative n=8 (69.4% threshold) and show n=6 and n=10 sensitivity; replace these scenario inputs if an organizer supplies actual attendance, margin, delivery/setup costs, or cancellation consequences.

## 2026-11-15: Lock the scored target and document diagnostics

* Target. Score the probability that the CoCoRaHS 24-hour report ending Sunday morning records at least 0.01 inches. The Saturday 7-9 p.m. class is the decision setting, not the event window being predicted. The canopy rule uses the wet-report probability; do not describe it as a class-hour rain forecast.
* Why and alternative. The Fairfax gauge has a daily label but no matched class-hour label in this dataset. I set aside the hourly class-time target until a local hourly observation can be obtained. Rain outside class can make a daily report wet even when it did not rain during class, so this proxy gap is not a residual the model can repair.
* Split and model. Keep the chronological cutoff because the decision is about future Saturdays; a random split could let later weather inform a past forecast. Use the two-input L2 logistic calibration as a small, interpretable adjustment to the training-rate baseline. Revisit if held-out calibration, a new NBM version, or more local observations change the decision.
* Loss. The rule compares $150 rent with p x $27 x n of expected loss without a canopy. At n=8, a missed wet report costs $216 and a dry-report rental costs $150; these remain illustrative gross-revenue assumptions, not organizer-specific costs.
* Reproducibility. Simulation seed 6002; training/held-out bootstrap seed 20261118. The bootstrap assumes independent Saturdays and does not represent NBM version shifts, proxy error, or future weather.
