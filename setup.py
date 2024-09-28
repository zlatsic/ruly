import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ruly',
    packages=['ruly'],
    version='0.0.5',
    url='https://github.com/ZlatSic/ruly',
    author='Zlatan Sičanica',
    author_email='zlatan.sicanica@gmail.com',
    description='Simple, extensible rule engine in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ])
