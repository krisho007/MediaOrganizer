from distutils.core import setup

setup(name='MediaOrganizer',
      version='1.0',
      description='Media Organizer',
      author='Krishna Kishor Kammaje',
      author_email='kammaje@outlook.com',
      url='',
      packages=['distutils', 'distutils.command','os','stat','datetime', 'tkinter', 'pathlib', 'exifread', 'shutil'],
     )