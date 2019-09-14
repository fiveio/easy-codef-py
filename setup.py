from setuptools import setup, find_packages

__title__ = 'easycodef'
__version__ = '0.0.1'
__author__ = 'mark(margurt)'
__copyright__ = 'Copyright 2019 margurt'

requires = None
with open('requirements.txt') as f:
   requires = f.read().strip().split('\n')

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email='dc7303@gmail.com',
    description='Easily develop codef api',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/dc7303/easy-codef-py.git',
    packages=find_packages(),
    keywords=[
        'easy-codef',
        'codef',
        'codef-api',
        'codef-py',
        'codef-python'
    ],
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requires
)