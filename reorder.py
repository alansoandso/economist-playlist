#!/usr/bin/env python
import os
import re
import shutil
import argparse

from itertools import count
from mutagen.id3 import ID3, TRCK

# My preferred order for the chapters
CHAPTERS = (
    'Introduction',
    'The world this week',
    'Science and technology',
    'Britain',
    'Leaders',
    'Briefing',
    'International',
    'Business',
    'Finance and economics',
    'Special report',
    'Europe',
    'United States',
    'Asia',
    'China',
    'Middle East and Africa',
    'The Americas',
    'Essay',
    'Books and arts',
    'Obituary'
)


def set_preferred_order(audio_files):
    # list of tuples: preferred order 'nn' and regex search pattern
    # e.g. ('02', re.compile('\\d{3}\\sScience and technology\\s'))
    re_chapters = [('{:02}'.format(order), re.compile('\\d{3}\\s' + chapter + '\\s')) for order, chapter in enumerate(CHAPTERS)]

    preferred = []
    for filename in audio_files:
        for index, regex in re_chapters:
            if regex.search(filename):
                # Prepend the preferred chapter number
                # e.g. '078 Science and technology - Recycling.mp3' to '02078 Science and technology - Recycling.mp3'
                destination = '{}{}'.format(index, filename)
                preferred.append((destination, filename))

    return preferred


def audio_paths(source, destination, preferred_files):
    for new, old in sorted(preferred_files):
        src = os.path.join(source, old)
        dest = os.path.join(destination, new)
        yield src, dest


def create_playlist(source, destination, preferred_files):
    return [(src, dest) for src, dest in audio_paths(source, destination, preferred_files) if not os.path.exists(dest)]


def make_preferred(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def copy_preferred(playlist):
    # Copy across the tracks in the preferred order and update the track number to reflect this order
    track = count(start=1)
    for s, d in playlist:
        shutil.copy(s, d)
        print('.', end='')
        # Get id3 tags and set the track number
        tags = ID3(d)
        tags["TRCK"] = TRCK(encoding=3, text=u'{}'.format(next(track)))
        tags.save(d)
    else:
        print('\nCopied {} files in playlist'.format(len(playlist)))


def find_audio_files(source):
    # Look for mp3 files in the downloads folder
    if not os.path.exists(source):
        print('No such originals: {}'.format(source))
        raise FileNotFoundError

    # a list of all the audio files
    return [file for file in os.listdir(source) if file.endswith('.mp3')]


def get_parser():
    parser = argparse.ArgumentParser(description='Re-order downloaded Economist audio files to my preferred playlist order')
    parser.add_argument('source', action="store", nargs='?', help='source folder of the economist latest download')
    parser.add_argument('destination', action="store", nargs='?', help='destination folder for the playlist')

    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['source']:
        source = os.path.abspath(args['source'])
    else:
        source = os.path.abspath('.')

    if args['destination']:
        destination = os.path.abspath(args['destination'])
    else:
        _, issue = os.path.split(source)
        destination = os.getenv('ECONOMIST_PATH') or os.path.join(os.getenv('HOME'), 'workspace', 'economist', issue)

    audio_files = find_audio_files(source)
    preferred_files = set_preferred_order(audio_files)
    playlist = create_playlist(source, destination, preferred_files)
    if playlist:
        make_preferred(destination)
    copy_preferred(playlist)

if __name__ == '__main__':
    command_line_runner()