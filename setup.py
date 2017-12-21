# Try using setuptools first, if it's installed
from setuptools import setup

# define all packages for distribution
packages = [
    'gpgraph',
]

setup(name='gpgraph',
      version='0.1.0',
      description='Genotype-phenotype maps in NetworkX.',
      author='Zach Sailer',
      author_email='zachsailer@gmail.com',
      url='https://github.com/harmslab/gpgraph',
      packages=packages,
      classifiers=[
        'Development Status :: 3 - Alpha',
      ],
      zip_safe=False)
