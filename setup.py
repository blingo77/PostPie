from setuptools import setup, find_packages

with open("README.md", "r") as i:
    description = i.read()

setup(
    name='PostPie',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary>=2.9.9'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)