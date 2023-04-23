
import mell.consts as c
import setuptools


long_description_content_type = "text/markdown"
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name=c.name,
    version=c.version,
    author=c.author,
    author_email=c.author_email,
    description=c.description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=c.url,
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

