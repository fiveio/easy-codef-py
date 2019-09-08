import src
from setuptools import setup, find_packages

setup(
    name=src.__title__,
    version=src.__version__,
    author=src.__author__,
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
    install_requires=[

    ]
)