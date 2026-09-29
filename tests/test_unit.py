"""Offline tests. No API key or network needed: python3 -m unittest"""
import tempfile, unittest
from pathlib import Path

import check_plan
from best_efforts import best_window
from intervals_common import blank_steps


class LactateCurve(unittest.TestCase):
    CURVE = [(200, 130), (300, 160), (400, 185)]

    def test_interpolates_between_points(self):
        self.assertAlmostEqual(check_plan.predicted_hr(250, self.CURVE), 145)

    def test_clamps_above_top_point(self):
        self.assertEqual(check_plan.predicted_hr(500, self.CURVE), 185)

    def test_below_first_point_scales_from_rest(self):
        hr = check_plan.predicted_hr(100, self.CURVE)
        self.assertTrue(60 < hr < 130)

    def test_no_curve_means_no_prediction(self):
        self.assertIsNone(check_plan.predicted_hr(250, []))

    def test_missing_csv_returns_empty(self):
        self.assertEqual(check_plan.load_curve("/nonexistent/lactate_curve.csv"), [])

    def test_csv_is_read_and_sorted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "curve.csv"
            p.write_text("watts,hr\n300,160\n200,130\n")
            self.assertEqual(check_plan.load_curve(p), [(200, 130), (300, 160)])


class BestEfforts(unittest.TestCase):
    def test_finds_the_hardest_window(self):
        watts = [100] * 60 + [400] * 30 + [100] * 60
        hr = [120] * 60 + [170] * 30 + [120] * 60
        w, h, start = best_window(watts, hr, 30)
        self.assertEqual((w, h, start), (400, 170, 60))

    def test_window_longer_than_ride(self):
        self.assertIsNone(best_window([200] * 10, [], 60))

    def test_gaps_count_as_zero_watts_and_hr_is_optional(self):
        w, h, _ = best_window([300, None, 300, 300], None, 2)
        self.assertEqual(w, 300)
        self.assertIsNone(h)


class Duplicates(unittest.TestCase):
    def test_flags_same_duration_and_load(self):
        a = {"moving_time": 3600, "icu_training_load": 60}
        b = {"moving_time": 3630, "icu_training_load": 62}
        self.assertEqual(len(check_plan.possible_duplicates([a, b])), 1)

    def test_ignores_different_rides(self):
        a = {"moving_time": 3600, "icu_training_load": 60}
        b = {"moving_time": 5400, "icu_training_load": 90}
        self.assertEqual(check_plan.possible_duplicates([a, b]), [])


class WorkoutSteps(unittest.TestCase):
    def test_blank_step_is_caught_inside_repeats(self):
        event = {"workout_doc": {"steps": [
            {"duration": 600, "power": {"value": 200}},
            {"reps": 3, "steps": [{"duration": 60, "power": {"value": 400}},
                                  {"duration": 60}]},
        ]}}
        self.assertEqual(len(blank_steps(event)), 1)

    def test_all_steps_have_targets(self):
        event = {"workout_doc": {"steps": [{"duration": 600, "power": {"value": 200}}]}}
        self.assertEqual(blank_steps(event), [])


if __name__ == "__main__":
    unittest.main()
