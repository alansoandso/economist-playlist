from unittest import TestCase, mock
import reorder


class TestEconomist(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_parser(self):
        with mock.patch('sys.argv', ['', 'Latest_Issue']):
            parser = reorder.get_parser()
            args = vars(parser.parse_args())
            self.assertEqual('Latest_Issue', args['source'])

    def test_get_audio_files(self):
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
                audio_files = reorder.find_audio_files('New_Issue')
                self.assertEqual(audio_files, expected)
                MockHelper.assert_called_with('New_Issue')

    def test_audio_files_directory_not_found(self):
        with mock.patch('reorder.os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError) as MockHelper:
                # reorder.find_audio_files('No_such_folder')
                reorder.find_audio_files('/')
                MockHelper.assert_called_with('No_such_folder')

    def test_set_preferred_order(self):
        # Generate a list of source/destination file paths
        mp3s = ['001 Introduction.mp3',
                '002 The world this week - Politics this week.mp3',
                '078 Science and technology - Recycling.mp3']
        expected = [('01002 The world this week - Politics this week.mp3', '002 The world this week - Politics this week.mp3'),
                    ('02078 Science and technology - Recycling.mp3', '078 Science and technology - Recycling.mp3')]

        actual = reorder.set_preferred_order(mp3s)
        self.assertEqual(actual, expected)

    def test_create_playlist(self):
        # Generate a list of destination/source file paths
        preferred = [('02078 Science and technology - Recycling.mp3', '078 Science and technology - Recycling.mp3'),
                     ('01002 The world this week - Politics this week.mp3', '002 The world this week - Politics this week.mp3')]

        expected = [('/old/New_Issue/002 The world this week - Politics this week.mp3',
                     '/new/New_Issue/01002 The world this week - Politics this week.mp3'),
                    ('/old/New_Issue/078 Science and technology - Recycling.mp3',
                     '/new/New_Issue/02078 Science and technology - Recycling.mp3')]

        actual = reorder.create_playlist('/old/New_Issue', '/new/New_Issue', preferred)
        self.assertEqual(actual, expected)

    @mock.patch('reorder.os.path.exists')
    def test_make_preferred_exists(self, mock_exists):
        mock_exists.return_value = True
        reorder.make_preferred('new')
        mock_exists.assert_called_once()

    @mock.patch('reorder.os.mkdir')
    @mock.patch('reorder.os.path.exists')
    def test_make_preferred_not_exists(self, mock_exists, mock_mkdir):
        mock_exists.return_value = False
        reorder.make_preferred('new')
        mock_exists.assert_called_once()
        mock_mkdir.assert_called_once()

    @mock.patch('reorder.shutil')
    @mock.patch('reorder.ID3')
    def test_copy_preferred(self, mock_id3, mock_shutil):
        playlist = [('/old/New_Issue/002 The world this week - Politics this week.mp3',
                     '/new/New_Issue/01002 The world this week - Politics this week.mp3'),
                    ('/old/New_Issue/078 Science and technology - Recycling.mp3',
                     '/new/New_Issue/02078 Science and technology - Recycling.mp3')]
        reorder.copy_preferred(playlist)
        self.assertTrue(mock_shutil.copy.call_count == len(playlist))
        self.assertTrue(mock_id3.call_count == len(playlist))
