# Ciccione-stimuli

A reproducible coordinate bank based on **Experiment 1** of Lorenzo Ciccione and Stanislas Dehaene (2021), *Can humans perform mental regression on a graph? Accuracy and bias in the perception of scatterplots*, Cognitive Psychology 128, 101406. Source: sections 2.1.2–2.1.4 of the supplied paper. These are newly generated stimuli, not the authors' original datasets.

## Generation

- X: `linspace(0, 1, n)`.
- Raw Y: `alpha * x + epsilon`, with independent Gaussian `epsilon ~ N(0, sigma²)` for each dot/trial.
- Center Y: subtract the sample mean and add 0.5, making the fitted regression pass through (0.5, 0.5).
- Regenerate a whole trial if a centered Y lies outside [-0.27, 1.27]. Do not clip points.
- No rejection based on observed slope, sign agreement, or residual variance. Noise may reverse the sign of a nonzero prescribed slope.
- Dot counts: 8, 10, 12, 14, 16, 18, 20, 22 (preserved from the original study bank at the user’s request, replacing the paper’s 6, 18, 38, 66). Noise standard deviations: 0.05, 0.10, 0.15, 0.20. Prescribed slopes: -0.1875, -0.125, -0.0625, 0, 0.0625, 0.125, 0.1875.
- Six blocks, each containing all 224 combinations once (1,344 main trials). Each repetition uses fresh noise. The task shuffles within each block.
- 25 independent practice stimuli use a seeded selection of 25 distinct parameter combinations.

`manifest.csv` and `manifest_training.csv` contain all coordinates at round-trip precision, prescribed slope, actual OLS slope, residual variance, prescribed category, observed trend category, and block identity. `metadata.json` records the seed and generator version context. No PNGs are needed: the temporal task renders these coordinate sequences directly.

Regenerate with Python and NumPy from any directory:

```sh
python /workspace/spatial-relation-study/Stimuli-Task/Ciccione-stimuli/generate.py
```

Default seed: 2021101401. To make a separate bank, use `--seed <integer> --output <another-directory>`; the browser uses the checked-in bank rather than regenerating for each participant.

## Explicit adaptations and interpretation

This is a **temporal adaptation**, not a reproduction of the original experiment. The paper showed complete scatterplots for 100 ms, used a 1000 ms fixation interval, and generated fresh datasets for each participant. Here dots appear sequentially at one horizontal location for nominally 200 ms each; the existing P/Q mapping, 500 ms response feedback, reminders, and downloadable responses are retained. Dot size stays at the current task's 11-reference-pixel setting; the paper's physical 2 mm dots cannot be reproduced without display calibration.

The paper describes boundary rejection before mentioning vertical centering, without detailing a second boundary check. This implementation checks the **final centered coordinates** against the stated display bounds, preventing off-screen points. That ordering is an explicit interpretation of the display constraint rather than a claim to match the original code.

Feedback uses the sign of the **observed OLS slope**, including when the prescribed slope is zero or noise reverses its sign. This is an adaptation to the existing per-trial feedback request; prescribed and observed slopes/categories are retained separately for analysis. It does not assert that the paper used this per-trial scoring rule. The paper provided aggregate feedback at block ends.

At 200 ms per dot, sequences last about 1.6–4.4 seconds. Main sequences total 4032 seconds (67.2 minutes), before responses, feedback, breaks, or practice. Browser timing can extend these durations. Actual onset times and sequence durations are recorded.

The original coordinate bank and `task.html` remain unchanged. The temporal page reads only this folder and includes `stimulusSet=Ciccione-stimuli` in response exports. No remote study data submission is configured.
