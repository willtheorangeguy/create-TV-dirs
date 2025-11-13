
import os
import shutil
import unittest
import subprocess
import sys

class TestTVShowOrganizer(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and dummy files for testing."""
        self.test_dir = "temp_test_dir"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        self.files_to_create = [
            "My Show (2023) - 01x01 - Pilot.mkv",
            "My Show (2023) - 01x02 - The Second One.mkv",
            "My Show (2023) - 02x01 - A New Season.mkv",
            "My Show (2023) - 00x01 - A Special Episode.mp4",
            "unrelated_file.txt",
            "documentary.avi"
        ]

        for filename in self.files_to_create:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("dummy content")

    def tearDown(self):
        """Remove the temporary directory after tests are done."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def run_script(self, args):
        """Helper function to run the organizer script as a subprocess."""
        base_command = [sys.executable, "-m", "tv_organizer"]
        command = base_command + args
        return subprocess.run(command, capture_output=True, text=True)

    def test_full_organization(self):
        """Test the default behavior: creating folders and moving files."""
        result = self.run_script([self.test_dir])
        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")

        # Check that folders were created
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Season 01")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Season 02")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Specials")))

        # Check that files were moved correctly
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Season 01", self.files_to_create[0])))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Season 01", self.files_to_create[1])))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Season 02", self.files_to_create[2])))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Specials", self.files_to_create[3])))

        # Check that unrelated files were not moved
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "unrelated_file.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "documentary.avi")))

    def test_dry_run(self):
        """Test the --dry-run flag to ensure no changes are made."""
        result = self.run_script([self.test_dir, "--dry-run"])
        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")
        self.assertIn("Dry Run Report", result.stdout)

        # Check that no folders were created
        self.assertFalse(os.path.isdir(os.path.join(self.test_dir, "Season 01")))
        self.assertFalse(os.path.isdir(os.path.join(self.test_dir, "Specials")))

        # Check that no files were moved
        for filename in self.files_to_create:
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

    def test_only_create_folders(self):
        """Test the --only-create-folders flag."""
        result = self.run_script([self.test_dir, "--only-create-folders"])
        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")
        self.assertIn("Creating Folders Only", result.stdout)

        # Check that folders were created
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Season 01")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Season 02")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "Specials")))

        # Check that no files were moved
        for filename in self.files_to_create:
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

if __name__ == "__main__":
    unittest.main()
