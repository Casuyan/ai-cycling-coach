"""Live tests against intervals.icu. Skipped unless .env has credentials.

    python3 -m unittest tests.test_integration              # read-only
    RUN_WRITE_TESTS=1 python3 -m unittest tests.test_integration   # also create + delete a workout
"""
import datetime, os, unittest

from intervals_common import athlete_get, blank_steps, create_workout, has_credentials, request

TODAY = datetime.date.today()


@unittest.skipUnless(has_credentials(), "no intervals.icu credentials in .env")
class ReadOnly(unittest.TestCase):
    def test_athlete_profile(self):
        me = athlete_get("")
        self.assertIn("id", me)

    def test_activities_have_the_fields_the_method_uses(self):
        acts = athlete_get(f"/activities?oldest={TODAY - datetime.timedelta(days=60)}&newest={TODAY}")
        self.assertIsInstance(acts, list)
        if not acts:
            self.skipTest("no activities in the last 60 days")
        keys = set().union(*(a.keys() for a in acts))
        for field in ("icu_training_load", "moving_time", "start_date_local"):
            self.assertIn(field, keys)
        with_power = [a for a in acts if a.get("icu_average_watts")]
        self.assertTrue(with_power, "no rides with power in the last 60 days: a power meter is required")

    def test_wellness_has_fitness_numbers(self):
        well = athlete_get(f"/wellness?oldest={TODAY - datetime.timedelta(days=7)}&newest={TODAY}")
        self.assertIsInstance(well, list)
        if well:
            self.assertIn("ctl", well[-1])
            self.assertIn("atl", well[-1])

    def test_events_endpoint(self):
        events = athlete_get(f"/events?oldest={TODAY}&newest={TODAY + datetime.timedelta(days=7)}")
        self.assertIsInstance(events, list)


@unittest.skipUnless(has_credentials() and os.environ.get("RUN_WRITE_TESTS") == "1",
                     "set RUN_WRITE_TESTS=1 to test writing to the calendar")
class WriteRoundTrip(unittest.TestCase):
    def test_create_parse_delete(self):
        date = (TODAY + datetime.timedelta(days=365)).isoformat()
        steps = "- 10m 150-180W\n\n3x\n- 2m 300W\n- 2m 150W\n\n- 5m 150W"
        created = create_workout(date, "ai-cycling-coach test (safe to delete)",
                                 "Created by tests/test_integration.py", steps)
        try:
            event = request("GET", f"/{created['id']}")
            self.assertTrue((event.get("workout_doc") or {}).get("steps"), "workout parsed to no steps")
            self.assertEqual(blank_steps(event), [], "some steps have no power target")
        finally:
            request("DELETE", f"/{created['id']}")


if __name__ == "__main__":
    unittest.main()
