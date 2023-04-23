
#import mell.consts as c
import setuptools

name = "mell"
version = "2.0.1"
author = "Diego Souza"
author_email = "diegofpsouza+mell@gmail.com"
url = "https://github.com/diegofps/pywup"

description = "A Metaprogramming Logic Layer designed to generate anything from template files"

long_description_content_type = "text/markdown"
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'mell = mell.main:main'
        ],
    },
    install_requires=[
        'jinja2'
    ],
    extras_require={
        "full": []
    }
)

