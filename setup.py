"""Setup remotepixel-tiler"""

from setuptools import setup, find_packages

# Runtime requirements.
inst_reqs = [
    "lambda-proxy-cache",
    "python-binary-memcached",
    "rio-color",
    "rio-tiler~=1.2",
]

extra_reqs = {}

setup(
    name="lambda-tiler-cache",
    version="0.0.1",
    description=u"""""",
    long_description=u"",
    python_requires=">=3",
    classifiers=["Programming Language :: Python :: 3.6"],
    keywords="",
    author=u"Vincent Sarago",
    author_email="contact@remotepixel.ca",
    url="https://github.com/vincentsarago/lambda-tiler-cache",
    license="BSD-3",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": ["lambda-tiler-cache = lambda_tiler_cache.scripts.cli:run"]
    },
)
