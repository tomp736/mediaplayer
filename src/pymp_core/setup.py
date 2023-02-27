import os
from setuptools import find_packages
from setuptools import setup

version = os.environ.get('APP_BUILD_VERSION', '0.0.1')

setup(
    name="pymp_core",
    description="",
    long_description=open("README.md").read(),
    url="",
    version=version,
    author="Thomas Pisula",
    author_email="tompisula@protonmail.com",
    packages=find_packages(exclude=["ez_setup"]),
    install_requires=open(
        os.path.join(os.path.dirname(__file__), "requirements.txt")
    ).readlines(),
    license="AGPL3",
)