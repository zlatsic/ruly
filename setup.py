import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('version.txt') as fh:
    version = fh.read()

setuptools.setup(
    name='ruly',
    packages=['ruly'],
    version=version,
    url='https://github.com/ZlatSic/ruly',
    author='Zlatan Sičanica',
    author_email='zlatan.sicanica@gmail.com',
    description='Simple, extensible rule engine in Python',
    long_description=long_description,
    long_description_content_type='text/markdown')
