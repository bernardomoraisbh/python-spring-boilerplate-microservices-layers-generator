import sys
import unittest
from unittest.mock import patch

sys.path.append("..")


from main import main


class TestMainFunction(unittest.TestCase):

    @patch('input_handler.gather_inputs', side_effect=['api.example.test', 'Person', 'US', 'String-firstName;Long-age', 'person_table', 'public', '11'])
    @patch('directory_handler.create_directories')
    @patch('builtins.print')
    def test_main_with_sample_inputs(self, mock_print, mock_create_directories, mock_gather_inputs):
        mock_gather_inputs.return_value = {
            'group_name': 'com.example',
            # ... other return values
        }

        mock_create_directories.return_value = "/path/to/package"

        main()  # Call your actual main function

        mock_print.assert_called_with("Operation completed")
        mock_create_directories.assert_called_with('com-example', 'com.example')

    # ... more test cases ...

if __name__ == '__main__':
    unittest.main()
