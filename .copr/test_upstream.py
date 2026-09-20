import unittest
from check_upstream import decide

COMMIT = "7f056a1ba23f3bf3b429155f53b59dd7721be629"

class DecisionTests(unittest.TestCase):
    def test_old_seven_character_and_new_twelve_character_versions(self):
        for version in ("0.6.1-0.20260521git7f056a1", "0.6.1^20240914212037git7f056a1ba23f-1"):
            build = {"id": 1, "state": "succeeded", "source_package": {"version": version}}
            self.assertFalse(decide(COMMIT, build, build)[0])
            self.assertTrue(decide("a" * 40, build, build)[0])
            self.assertTrue(decide(COMMIT, build, build, force=True)[0])

    def test_active_builds_are_never_duplicated(self):
        for state in ("pending", "running", "importing", "starting"):
            self.assertFalse(decide(COMMIT, {"id": 1, "state": state}, None, force=True)[0])

    def test_failed_builds_are_retried(self):
        for state in ("failed", "canceled", "skipped"):
            self.assertTrue(decide(COMMIT, {"id": 1, "state": state}, None)[0])

    def test_missing_build_is_built(self):
        self.assertTrue(decide(COMMIT, None, None)[0])
