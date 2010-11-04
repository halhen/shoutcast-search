from setuptools import setup, find_packages


setup(
    name = 'shoutcast_search',
    version = '0.4',
    url = 'http://github.com/halhen/shoutcast-search',
    author = 'Henrik Hallberg',
    author_email = 'halhen@k2h.se',
    license = 'GPL',
    packages = find_packages(),
    install_requires = [],
    description = 'Search shoutcast.com web radio stations',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        ],
    )
