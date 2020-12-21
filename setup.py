from setuptools import find_packages, setup
import os, sys

NAME = 'livy-connect'
VERSION='0.0.1'
DESCRIPTION=''
AUTHOR='hari prasad',
AUTHOR_EMAIL='hphari1998@gmail.com',
packages=['livy_connect']

requires = [
    'requests'
]

test_requirements = [
    'pytest-httpbin==0.0.7',
    'pytest-cov',
    'pytest-mock',
    'pytest-xdist',
    'PySocks>=1.5.6, !=1.5.7',
    'pytest>=3'
]

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name= NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=packages,
    license='',
    install_requires=requires
)



# 'setup.py build' shortcut.
if sys.argv[-1].lower() == 'build':
    os.system('python setup.py sdist bdist_wheel --universal')
    # os.system('twine upload dist/*')
    sys.exit()
