from unittest import TestCase, mock
from reorder import Economist, get_parser, set_preferred_order


class TestEconomist(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.economist = Economist('New_Issue')

    def test_get_parser(self):
        with mock.patch('sys.argv', ['', 'Latest_Issue']):
            parser = get_parser()
            args = vars(parser.parse_args())
            self.assertEqual('Latest_Issue', args['download_folder'])

    def test_audio_files(self):
        # Return a list of only  mp3 file names
        mp3s = ['not an mp3 file',
                '001 Introduction.mp3',
                '002 The world this week - Politics this week.mp3',
                '078 Science and technology - Recycling.mp3']

        expected = ['001 Introduction.mp3',
                    '002 The world this week - Politics this week.mp3',
                    '078 Science and technology - Recycling.mp3']

        with mock.patch('reorder.os.listdir', return_value=mp3s):
            with mock.patch('reorder.os.path.exists', return_value=True) as MockHelper:
                economist = Economist('New_Issue')
                economist.find_audio_files()
                self.assertEqual(economist.file_list, expected)
                MockHelper.assert_called_with('New_Issue')

    def test_audio_files_directory_not_found(self):
        with mock.patch('reorder.os.path.exists', return_value=False) as MockHelper:
            economist = Economist('No_such_folder')
            self.assertRaises(FileNotFoundError, economist.find_audio_files)
            MockHelper.assert_called_with('No_such_folder')

    def test_set_preferred_order(self):
        # Generate a list of source/destination file paths
        mp3s = ['001 Introduction.mp3',
                '002 The world this week - Politics this week.mp3',
                '078 Science and technology - Recycling.mp3']
        expected = [('/Users/alan/workspace/economist/New_Issue/01002 The world this week - Politics this week.mp3', 'New_Issue/002 The world this week - Politics this week.mp3'),
                    ('/Users/alan/workspace/economist/New_Issue/02078 Science and technology - Recycling.mp3', 'New_Issue/078 Science and technology - Recycling.mp3')]

        with mock.patch('reorder.os.listdir', return_value=mp3s):
            with mock.patch('reorder.os.path.exists', return_value=True) as MockHelper:
                self.economist.find_audio_files()
                self.economist.set_preferred_order()
                self.assertEqual(self.economist.source_destination_paths, expected)
                MockHelper.assert_called_with('/Users/alan/workspace/economist/New_Issue')

    def test_set_playlist_order(self):
        # Generate a list of destination/source file paths
        mp3s = ['001 Introduction.mp3',
                '002 The world this week - Politics this week.mp3',
                '078 Science and technology - Recycling.mp3']
        expected = [('/new destination folder/New_Issue/01002 The world this week - Politics this week.mp3',
                     '/origin folder/002 The world this week - Politics this  week.mp3'),
                    ('/new destination folder/New_Issue/02078 Science and technology - Recycling.mp3',
                     '/origin folder/078 Science and technology - Recycling.mp3')]

        # actual = set_preferred_order('/origin folder', mp3s)
        # self.assertEqual(actual, expected)
