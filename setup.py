from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    race_license = f.read()

setup(
    name='race',
    version='1.0',
    description='Race imitation',
    long_description=readme,
    author='val0907010',
    author_email='val0907010@gmail.com',
    url='https://github.com/',
    license=race_license,
    packages=find_packages(exclude=('tests', 'docs'))
)
