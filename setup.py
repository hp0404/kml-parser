from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.1.0"


def get_long_description():
    readme = Path(__file__).resolve().parent / "README.md"
    return readme.read_text()


setup(
    name="kmlparser",
    description="A library for parsing KML files",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/hp0404/kmlparser",
    project_urls={
        "Issues": "https://github.com/hp0404/kmlparser/issues",
    },
    license="MIT",
    version=VERSION,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["beautifulsoup4>=4.10", "lxml>=4.9"],
    extras_require={
        "testing": ["pytest", "pre-commit"],
    },
)
