from distutils.core import setup

install_requires = [
    'mutagen==1.41.1'
]

setup(name='reorder',
      version='0.0.1',
      description='Reorder the economist audio file into my preferred playlist',
      author='Alan So',
      author_email='alansoandso@gmail.com',
      packages=['reorder'],
      scripts=['scripts/reorder'],
      install_requires=install_requires,
      )