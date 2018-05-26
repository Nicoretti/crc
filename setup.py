from setuptools import setup, find_packages
from crc.crc import LIBRARY_VERSION

setup(
    name='crc',
    version=LIBRARY_VERSION,
    packages=find_packages(),
    install_requires=['docopt'],
    url='https://github.com/Nicoretti/crc',
    license='BSD',
    author='Nicola Coretti',
    author_email='nico.coretti@gmail.com',
    description='TBD',
    keywords=['CRC', 'CRC8', 'CRC16', 'CRC32'],
    entry_points={
        'console_scripts': [
            'crc=crc.tools:main',
        ],
        'crc.cli.command': ['table=crc.tools:table']
    }
)
