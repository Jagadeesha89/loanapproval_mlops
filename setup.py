"""
The setup.py file is an essential part of packaging and 
distirbuting python projects. It is used by setuptools
(or distutils in older python version) to define the configuration
of your projects, such as its meta data,dependencies,and more

"""

from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:
    requirements_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirements=line.strip()
                if requirements and requirements != '-e .':
                    requirements_lst.append(requirements)
    except FileNotFoundError:
        print("Requirements.txt file not found in the current directory")

    return requirements_lst

setup(
    name="Loanapproval",
    version="0.0.1",
    author="Jagadeesha",
    author_email="jaga.m.gowda@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)



