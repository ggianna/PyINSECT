import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pyinsect-ggianna",
    version="0.0.36",
    author="George Giannakopoulos",
    author_email="ggianna@iit.demokritos.gr",
    description="A python port of the JInsect toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/npit/PyINSECT",
    packages=['pyinsect', 'pyinsect.collector', 'pyinsect.documentModel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
