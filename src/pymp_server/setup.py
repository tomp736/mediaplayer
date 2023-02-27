import os
from setuptools import find_packages
from setuptools import setup

version = os.environ.get('APP_BUILD_VERSION', '0.0.1')

setup(
    name="pymp_server",
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
    entry_points={"console_scripts": ["pymp_server  = pymp_server.__main__:main"]},
    license="AGPL3",
)