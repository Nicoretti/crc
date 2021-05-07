import pathlib
import unittest
from crc import LIBRARY_VERSION
from setuptools import setup

current = pathlib.Path(__file__).parent.resolve()


def tests():
    return unittest.defaultTestLoader.discover(start_dir=f'{current.resolve()}', pattern='*test*.py')


def readme():
    return (current / 'README.md').read_text(encoding='utf-8')


if __name__ == '__main__':
    setup(
        name='crc',
        version=LIBRARY_VERSION,
        test_suite='setup.tests',
        py_modules=['crc'],
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        url='https://github.com/Nicoretti/crc',
        license='BSD',
        author='Nicola Coretti',
        author_email='nico.coretti@gmail.com',
        description='Library and CLI to calculate and verify all kinds of CRC checksums.',
        keywords=['CRC', 'CRC8', 'CRC16', 'CRC32', 'CRC64'],
        long_description=readme(),
        long_description_content_type='text/markdown',
        entry_points={
            'console_scripts': [
                'crc=crc:main',
            ],
        }
    )
