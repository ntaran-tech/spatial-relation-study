#!/usr/bin/env python3
"""Reproducible Experiment 1 stimulus bank; see README.md for adaptations."""
import argparse
import csv
import itertools
import json
from pathlib import Path

import numpy as np

SLOPES = [-0.1875, -0.125, -0.0625, 0.0, 0.0625, 0.125, 0.1875]
COUNTS = [8, 10, 12, 14, 16, 18, 20, 22]
SIGMAS = [0.05, 0.1, 0.15, 0.2]
Y_MIN, Y_MAX = -0.27, 1.27
DEFAULT_SEED = 2021101401


def stimulus(rng, index, block, n, alpha, sigma, kind):
    x = np.linspace(0, 1, n)
    retries = 0
    while True:
        y = alpha * x + rng.normal(0, sigma, n)
        y = y - y.mean() + 0.5
        # Apply the paper's display bounds to the centered, displayed coordinates.
        if np.all((y >= Y_MIN) & (y <= Y_MAX)):
            break
        retries += 1
    # Store round-trip precision; category is based on these same saved coordinates.
    observed = float(np.dot(x - x.mean(), y - y.mean()) / np.sum((x - x.mean()) ** 2))
    residuals = y - (observed * (x - x.mean()) + y.mean())
    return dict(index=index, block=block, stimulus_type=kind, n=n, slope=alpha,
                sigma=sigma, observed_slope=observed,
                residual_variance=float(np.var(residuals)),
                trend_category='Trend_Up' if observed > 0 else 'Trend_Down',
                prescribed_category='Trend_Up' if alpha > 0 else ('Trend_Down' if alpha < 0 else 'Zero'),
                dot_size_px=11, out_of_bounds_retries=retries,
                x_values=','.join(format(v, '.17g') for v in x),
                y_values=','.join(format(v, '.17g') for v in y))


def generate(output, seed=DEFAULT_SEED):
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    combinations = list(itertools.product(COUNTS, SLOPES, SIGMAS))
    main = []
    for block in range(1, 7):
        for n, alpha, sigma in combinations:
            main.append(stimulus(rng, len(main), block, n, alpha, sigma, 'main'))
    # Independent practice examples, spread across the full design.
    practice = [stimulus(rng, i, 0, *combinations[j], 'training')
                for i, j in enumerate(rng.permutation(len(combinations))[:25])]
    for name, rows in [('manifest.csv', main), ('manifest_training.csv', practice)]:
        with (output / name).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    metadata = dict(stimulus_set='Ciccione-stimuli', seed=seed,
                    numpy_version=np.__version__, experiment=1,
                    source='Ciccione & Dehaene (2021), Cognitive Psychology 128, 101406, sections 2.1.2–2.1.4',
                    slopes=SLOPES, dot_counts=COUNTS, sigmas=SIGMAS,
                    dot_count_adaptation="original study bank counts; paper used [6, 18, 38, 66]",
                    blocks=6, trials_per_block=len(combinations), main_trials=len(main), practice_trials=len(practice),
                    bounds=[Y_MIN, Y_MAX], bounds_applied='after vertical centering',
                    feedback_basis='sign of observed OLS slope',
                    independently_generated_per_participant=False)
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Generated {len(main)} main and {len(practice)} practice stimuli in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    generate(args.output, args.seed)
