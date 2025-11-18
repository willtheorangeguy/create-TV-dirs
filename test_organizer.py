
import os
import shutil
import unittest
import subprocess
import sys
from tv_organizer.__main__ import get_organization_plan

class TestGetOrganizationPlan(unittest.TestCase):
    """Unit tests for the get_organization_plan function."""

    def setUp(self):
        """Set up a temporary directory and dummy files for testing."""
        self.test_dir = "temp_unit_test_dir"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        """Remove the temporary directory after tests are done."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_nonexistent_directory(self):
        """Test that non-existent directories are handled correctly."""
        actions, error = get_organization_plan("/nonexistent/path")
        self.assertIsNone(actions)
        self.assertIn("Directory not found", error)

    def test_empty_directory(self):
        """Test that empty directories are handled correctly."""
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(actions)
        self.assertIn("No files to organize", error)

    def test_no_matching_files(self):
        """Test that directories with no matching files are handled correctly."""
        # Create files without season format
        with open(os.path.join(self.test_dir, "random_file.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(self.test_dir, "another.mp4"), "w") as f:
            f.write("content")
        
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(actions)
        self.assertIn("No files with the expected season format", error)

    def test_single_season(self):
        """Test organizing files from a single season."""
        files = [
            "Show.01x01.mkv",
            "Show.01x02.mkv",
            "Show.01x03.mkv"
        ]
        for filename in files:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("content")
        
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(error)
        self.assertIsNotNone(actions)
        self.assertIn("Season 01", actions)
        self.assertEqual(len(actions["Season 01"]), 3)

    def test_multiple_seasons(self):
        """Test organizing files from multiple seasons."""
        files = [
            "Show.01x01.mkv",
            "Show.01x02.mkv",
            "Show.02x01.mkv",
            "Show.03x05.mkv"
        ]
        for filename in files:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("content")
        
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(error)
        self.assertIsNotNone(actions)
        self.assertIn("Season 01", actions)
        self.assertIn("Season 02", actions)
        self.assertIn("Season 03", actions)
        self.assertEqual(len(actions["Season 01"]), 2)
        self.assertEqual(len(actions["Season 02"]), 1)
        self.assertEqual(len(actions["Season 03"]), 1)

    def test_specials_folder(self):
        """Test that season 00 is mapped to 'Specials' folder."""
        files = [
            "Show.00x01.mkv",
            "Show.00x02.mkv"
        ]
        for filename in files:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("content")
        
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(error)
        self.assertIsNotNone(actions)
        self.assertIn("Specials", actions)
        self.assertEqual(len(actions["Specials"]), 2)

    def test_mixed_files(self):
        """Test that only files with season format are included."""
        files = [
            "Show.01x01.mkv",
            "random.txt",
            "Show.02x01.mp4",
            "another_file.avi"
        ]
        for filename in files:
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write("content")
        
        actions, error = get_organization_plan(self.test_dir)
        self.assertIsNone(error)
        self.assertIsNotNone(actions)
        # Only 2 files should be in the actions
        total_files = sum(len(file_list) for file_list in actions.values())
        self.assertEqual(total_files, 2)


class TestTVShowOrganizer(unittest.TestCase):
    """Integration tests for the TV show organizer script."""

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
