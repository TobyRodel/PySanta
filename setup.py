from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='pysanta',
    version='0.0.1',
    description='A Python module for organising secret Santa gift exchanges.',
    long_description=readme,
    author='Toby Rodel',
    author_email='trodel01@qub.ac.uk',
    url='https://github.com/TobyRodel/pysanta',
    license='MIT',
    packages=['pysanta']
)