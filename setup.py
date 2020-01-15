from __future__ import absolute_import
from setuptools import setup
from setuptools import find_packages

setup(name='entropymdlp',
      version='0.1',
      description='Minimum description length principle',
      url='http://github.com/maxpumperla/entropy-mdlp',
      download_url='https://github.com/maxpumperla/entropy-mdlp/tarball/0.1',
      author='Max Pumperla',
      author_email='max.pumperla@googlemail.com',
      install_requires=['numpy'],

      packages=find_packages(),
      license='MIT',
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ])
