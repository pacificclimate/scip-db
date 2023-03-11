import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

__version__ = (0, 0, 1)

setup(
    name="salmon_occurrence",
    description="An ORM representation of the SCIP salmon population database",
    keywords="sql database",
    packages=find_packages(include=["salmon_occurrence"]),
    version=".".join(str(d) for d in __version__),
    url="http://www.pacificclimate.org/",
    author="James Hiebert",
    author_email="hiebert@uvic.ca",
    zip_safe=True,
    install_requires=[
        "alembic",
        "geoalchemy2",
        "psycopg2",
        "SQLAlchemy",
    ],
    classifiers="""Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Internet
Topic :: Scientific/Engineering
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules""".split(
        "\n"
    ),
)