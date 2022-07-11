import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="configs_generator",
    version="0.0.7",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="Configuration generation from Excel Facts File",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliasgar1978/configs_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires= ['pandas','xlrd', 'nettoolkit']
)

