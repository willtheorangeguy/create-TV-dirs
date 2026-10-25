from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tv_organizer.__main__ import move_without_overwrite


class MoveSafetyTests(unittest.TestCase):
    def test_existing_destination_preserves_both_files(self):
        with tempfile.TemporaryDirectory() as directory:
            source, destination = Path(directory) / "source", Path(directory) / "destination"
            source.write_bytes(b"new episode")
            destination.write_bytes(b"original episode")
            with self.assertRaises(FileExistsError):
                move_without_overwrite(source, destination)
            self.assertEqual(source.read_bytes(), b"new episode")
            self.assertEqual(destination.read_bytes(), b"original episode")

    def test_failed_copy_preserves_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source, destination = Path(directory) / "source", Path(directory) / "destination"
            source.write_bytes(b"episode")
            with patch("tv_organizer.__main__.shutil.copyfileobj", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    move_without_overwrite(source, destination)
            self.assertEqual(source.read_bytes(), b"episode")
            self.assertFalse(destination.exists())
