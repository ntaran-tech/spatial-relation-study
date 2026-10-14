"""Run with: python -m unittest discover -s Stimuli-Task/Ciccione-stimuli."""
import csv
import importlib.util
import itertools
from pathlib import Path
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ciccione_generator', ROOT / 'generate.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class StimulusTests(unittest.TestCase):
    def test_saved_design_and_coordinates(self):
        with (ROOT / 'manifest.csv').open() as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 672)
        design = set(itertools.product(generator.COUNTS, generator.SLOPES, generator.SIGMAS))
        for block in range(1, 7):
            group = [r for r in rows if int(r['block']) == block]
            self.assertEqual(len(group), 112)
            self.assertEqual({(int(r['n']), float(r['slope']), float(r['sigma'])) for r in group}, design)
        with (ROOT / 'manifest_training.csv').open() as f:
            practice = list(csv.DictReader(f))
        self.assertEqual(len(practice), 25)
        for row in rows + practice:
            n = int(row['n'])
            x = np.fromstring(row['x_values'], sep=',')
            y = np.fromstring(row['y_values'], sep=',')
            np.testing.assert_allclose(x, np.linspace(0, 1, n), atol=1e-14)
            self.assertEqual(len(y), n)
            self.assertAlmostEqual(y.mean(), 0.5, places=13)
            self.assertTrue(np.all((y >= -0.27) & (y <= 1.27)))
            actual = np.polyfit(x, y, 1)[0]
            self.assertAlmostEqual(actual, float(row['observed_slope']), places=12)
            self.assertEqual(row['trend_category'], 'Trend_Up' if actual > 0 else 'Trend_Down')
        # Verify that the old sign-rejection filter did not leak into this generator.
        self.assertTrue(any(float(r['slope']) * float(r['observed_slope']) < 0 for r in rows))
        zero = [float(r['observed_slope']) for r in rows if float(r['slope']) == 0]
        self.assertTrue(any(v > 0 for v in zero) and any(v < 0 for v in zero))

    def test_reproducibility(self):
        with tempfile.TemporaryDirectory() as d:
            generator.generate(Path(d))
            for filename in ['manifest.csv', 'manifest_training.csv', 'metadata.json']:
                self.assertEqual((Path(d) / filename).read_bytes(), (ROOT / filename).read_bytes())


if __name__ == '__main__':
    unittest.main()
