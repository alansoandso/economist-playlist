from setuptools import setup

install_requires = [
    'mutagen==1.41.1'
]

setup(name='reorder',
      version='0.1.0',
      description='Reorder the economist audio file into my preferred playlist',
      author='Alan So',
      author_email='alansoandso@gmail.com',
      scripts=['reorder', 'reorder.py'],
      install_requires=install_requires,
      )