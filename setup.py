from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in em_member/__init__.py
from em_member import __version__ as version

setup(
	name="em_member",
	version=version,
	description="Ema membership management",
	author="360ground",
	author_email="gedewon@360ground.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
