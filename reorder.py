#!/usr/bin/env python
import os
import re
import shutil
import argparse
from itertools import count

from mutagen.id3 import ID3, TRCK


chapters = {
    'Introduction': '00',
    'The world this week': '01',
    'Leaders': '04',
    'Letters': '18',
    'Briefing': '05',
    'United States': '11',
    'The Americas': '15',
    'Asia': '12',
    'China': '13',
    'Middle East and Africa': '14',
    'Europe': '10',
    'Britain': '03',
    'International': '06',
    'Business': '07',
    'Finance and economics': '08',
    'Science and technology': '02',
    'Books and arts': '17',
    'Obituary': '18',
    'Essay': '16',
    'Special report': '09'
}
# Create a list of tuples containing preferred order 'nn' and its regex pattern
chapter_orders = [(order, re.compile('\\d{3}\\s' + chapter + '\\s')) for chapter, order in chapters.items()]
economist_root = "/Users/alan/workspace/economist"


class Economist():
    def __init__(self, source_folder):
        self.download_folder = source_folder
        self.source_destination_paths = []
        self.file_list = []

    def find_audio_files(self):
        # Look for mp3 files in the download folder
        if not os.path.exists(self.download_folder):
            print('No such download_folder: {}'.format(self.download_folder))
            raise FileNotFoundError

        # a list of all the audio files
        self.file_list = [filename for filename in os.listdir(self.download_folder) if filename.endswith('.mp3')]

    def set_preferred_order(self):
        _, latest = os.path.split(self.download_folder)
        latest_issues = os.path.join(economist_root, latest)

        for filename in self.file_list:
            for index, chapter in chapter_orders:
                if chapter.search(filename):
                    source = os.path.join(self.download_folder, filename)
                    # Prepend the preferred chapter number
                    # e.g. '078 Science and technology - Recycling.mp3' to '02078 Science and technology - Recycling.mp3'
                    destination = os.path.join(latest_issues, '{}{}'.format(index, filename))
                    self.source_destination_paths.append((destination, source))

        # Create a folder to hold only the tracks I want
        if not os.path.exists(latest_issues) and self.source_destination_paths:
            print('Creating folder: {}'.format(latest_issues))
            os.mkdir(latest_issues)

    def create_playlist(self):
        # Copy across the tracks in the preferred order and update the track number to reflect this order
        track = count(start=1)
        for destination, source in sorted(self.source_destination_paths):
            if not os.path.exists(destination):
                shutil.copy(source, destination)
                print('.', end='')
                # print source, destination
                # Get id3 tags and set the track number
                tags = ID3(destination)
                tags["TRCK"] = TRCK(encoding=3, text=u'{}'.format(next(track)))
                tags.save(destination)
            else:
                print(destination)
        print('done')


def get_latest_issues(download_folder):
    _, latest = os.path.split(download_folder)
    return os.path.join(economist_root, latest)


def set_preferred_order(latest_issues, file_list):
    source_destination_paths = []
    for filename in file_list:
        for index, chapter in chapter_orders:
            if chapter.search(filename):
                source = os.path.join(latest_issues, filename)
                # Prepend the preferred chapter number
                # e.g. '078 Science and technology - Recycling.mp3' to '02078 Science and technology - Recycling.mp3'
                destination = os.path.join(latest_issues, '{}{}'.format(index, filename))
                source_destination_paths.append((destination, source))


def find_audio_files(self):
    # Look for mp3 files in the download folder
    if not os.path.exists(self.download_folder):
        print('No such download_folder: {}'.format(self.download_folder))
        raise FileNotFoundError

    # a list of all the audio files
    self.file_list = [filename for filename in os.listdir(self.download_folder) if filename.endswith('.mp3')]


def get_parser():
    parser = argparse.ArgumentParser(description='Re-order downloaded Economist audio files to my preferred playlist order')
    parser.add_argument('download_folder', action="store", nargs='?', help='source folder of the economist latest download')

    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if not args['download_folder']:
        args['download_folder'] = os.path.abspath('.')

    latest_issue = Economist(args['download_folder'])
    latest_issue.find_audio_files()
    latest_issue.set_preferred_order()
    latest_issue.create_playlist()


if __name__ == '__main__':
    command_line_runner()