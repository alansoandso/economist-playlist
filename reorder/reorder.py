#!/usr/bin/env python
from __future__ import print_function

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
    'United States': '10',
    'The Americas': '14',
    'Asia': '11',
    'China': '12',
    'Middle East and Africa': '13',
    'Europe': '09',
    'Britain': '03',
    'International': '06',
    'Business': '07',
    'Finance and economics': '08',
    'Science and technology': '02',
    'Books and arts': '16',
    'Obituary': '17',
    'Essay': '15'
}

economist_root = "/Users/alan/workspace/economist"


def audiofile_list(directory):
    if not os.path.exists(directory):
        print('No such directory: {}'.format(directory))
        return

    _, latest = os.path.split(directory)

    file_list = [filename for filename in os.listdir(directory) if filename.endswith('.mp3')]
    # 'nn', regex pattern
    chapter_orders = [(order, re.compile('\d{3}\s' + chapter + '\s')) for chapter, order in chapters.items()]

    src_dsts = []
    latest_issue = os.path.join(economist_root, latest)
    for filename in file_list:
        for index, chapter in chapter_orders:
            if chapter.search(filename):
                source = os.path.join(directory, filename)
                # Prepend the preferred chapter number
                # e.g. '078 Science and technology - Recycling.mp3' to '02078 Science and technology - Recycling.mp3'
                destination = os.path.join(latest_issue, '{}{}'.format(index, filename))
                src_dsts.append((destination, source))

    # Create a folder to hold only the tracks I want
    if not os.path.exists(latest_issue):
        print('Creating folder: {}'.format(latest_issue))
        os.mkdir(latest_issue)

    # Copy across the tracks in the preferred order and update the track number to reflect this order
    track = count(start=1)
    for destination, source in sorted(src_dsts):
        if not os.path.exists(destination):
            shutil.copy(source, destination)
            print('.', end='')
            # print source, destination
            # Get id3 tags and set the track number
            tags = ID3(destination)
            tags["TRCK"] = TRCK(encoding=3, text=u'{}'.format(next(track)))
            tags.save(destination)

    print('done')


def run():
    parser = argparse.ArgumentParser(description='Reorder a directory full of economist audio files to my playlist')
    parser.add_argument('directory', action="store", nargs='?', help='starting directory')

    args = parser.parse_args()

    if args.directory:
        audiofile_list(os.path.abspath(args.directory))
    else:
        audiofile_list(os.path.abspath('.'))


if __name__ == '__main__':
    run()

