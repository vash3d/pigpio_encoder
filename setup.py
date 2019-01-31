from setuptools import setup, find_packages

from codecs import open
from os import path

file_path = path.abspath(path.dirname(__file__))

with open(path.join(file_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pigpio_encoder',
      version='0.2.0',
      description='Python module for for quickly interface a KY040 rotary encoder with Raspberry Pi.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
      ],
      keywords='rotary encoder switch ky040 gpio raspberry',
      url='https://github.com/vash3d/pigpio_encoder',
      author='vash',
      author_email='vash.3d@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
