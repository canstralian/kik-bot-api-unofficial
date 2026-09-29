from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.5.0"
DESCRIPTION = "Python API for writing unoffical kik bots that act like humans"

setup(
    name="kik_unofficial",
    version=VERSION,
    author="Tomer",
    author_email="tomer8007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/tomer8007/kik-bot-api-unofficial",
    download_url="https://github.com/tomer8007/kik-bot-api-unofficial/tarball/new",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    keywords=[
        "kik",
        "bot",
        "kikbot",
        "kik-messenger-platform",
        "api",
        "unofficial",
        "python",
    ],
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.10,<3.12",
    install_requires=[
        "pbkdf2",
        "rsa",
        "lxml>=5.4,<7",
        "bs4",
        "protobuf>=4.25.8,<6",
        "requests>=2.32.4,<3",
        "pillow>=10.4,<12",
        "pyDes",
        "python-dotenv",
        "PyYAML>=6.0.2,<7",
        "defusedxml>=0.7.1,<1",
        "beautifulsoup4>=4.12.3,<5",
        "colorama",
    ],
    extras_require={"dev": [], "test": []},
    package_data={"kik_unofficial": []},
    # No console entry point: kik_unofficial.cmdline does not exist.
)
