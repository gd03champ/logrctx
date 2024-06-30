from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name="logrctx",
    version="0.1",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        "console_scripts": [
            "logrctx=logrctx.main:app",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.py"],
    },
)
