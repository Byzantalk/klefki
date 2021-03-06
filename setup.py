import os
import platform
from setuptools import setup, find_packages, Extension

here = os.path.abspath(os.path.dirname(__file__))
platform = platform.python_implementation()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]
author = 'Ryan Kung'
email = 'ryankung@ieee.org'


setup(
    name='klefki',
    description="Klefki is a playground for researching elliptic curve group based algorithms & applications, such as MPC, HE, ZKP, and Bitcoin/Ethereum. All data types & structures are based on mathematical defination of abstract algebra.",  # noqa
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ZeroProphet/klefki',
    version='1.7.1',
    packages=find_packages(here, exclude=['tests', "notes"]),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography"
    ],
    entry_points={
        'console_scripts': [
            'klefki=klefki.client.shell:main'
        ]
    }
)
