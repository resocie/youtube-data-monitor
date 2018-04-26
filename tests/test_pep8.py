import unittest
import pycodestyle


class TestCodeFormat(unittest.TestCase):

    def test_conformance_core_output(self):
        """Test that we conform to PEP-8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['core/output.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_conformance_core_actors_info(self):
        """Test that we conform to PEP-8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['core/actors_info.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
