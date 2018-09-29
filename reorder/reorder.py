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
    def __init__(self):
        self.download_folder = ''
        self.source_destination_paths = []
        self.file_list = []

    def get_source(self):
        parser = argparse.ArgumentParser(description='Re-order downloaded Economist audio files to my preferred playlist order')
        parser.add_argument('download_folder', action="store", nargs='?', help='download folder')
        args = parser.parse_args()
        self.download_folder = args.download_folder if args.download_folder else os.path.abspath('.')

    def find_audio_files(self):
        # Look for mp3 files in the download folder
        if not os.path.exists(self.download_folder):
            print('No such download_folder: {}'.format(self.download_folder))
            raise FileNotFoundError

        # a list of all the audio files
        self.file_list = [filename for filename in os.listdir(self.download_folder) if filename.endswith('.mp3')]

    def set_preferred_order(self):
        _, latest = os.path.split(self.download_folder)
        latest_issue = os.path.join(economist_root, latest)
        for filename in self.file_list:
            for index, chapter in chapter_orders:
                if chapter.search(filename):
                    source = os.path.join(self.download_folder, filename)
                    # Prepend the preferred chapter number
                    # e.g. '078 Science and technology - Recycling.mp3' to '02078 Science and technology - Recycling.mp3'
                    destination = os.path.join(latest_issue, '{}{}'.format(index, filename))
                    self.source_destination_paths.append((destination, source))

        # Create a folder to hold only the tracks I want
        if not os.path.exists(latest_issue):
            print('Creating folder: {}'.format(latest_issue))
            os.mkdir(latest_issue)

    def create(self):
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

if __name__ == '__main__':
    my_playlist = Economist()
    my_playlist.get_source()
    my_playlist.find_audio_files()
    my_playlist.set_preferred_order()
    my_playlist.create()

