import setuptools
import timey

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='timey',
    version=timey.__version__,
    author="Haran Rajkumar",
    author_email="haranrajkumar97@gmail.com",
    description="CLI timer app to keep track of your life",
    long_description_content_type="text/markdown",
    url="https://github.com/haranrk/",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        timey=timey.timey:main
    ''',     
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],   
    
)