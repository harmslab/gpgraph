# Try using setuptools first, if it's installed
from setuptools import setup

# define all packages for distribution
packages = [
    'gpgraph',
]

setup(name='gpgraph',
      version='0.1.0',
      description='A Python library for creating NetworkX objects from GenotypePhenotypeMap objects.',
      author='Zach Sailer',
      author_email='zachsailer@gmail.com',
      url='https://github.com/harmslab/gpgraph',
      packages=packages,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
      ],
      zip_safe=False)
