import os

from setuptools import setup, find_packages


# Helper function to read the requirements.txt file
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r') as file:
        return file.read().splitlines()


# Reading the long description from README.md
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'r') as file:
        return file.read()


setup(
    name='CLIPhone',
    version='0.1.0',
    author='Andrii Vynar, Anatolii Huryk, Artur Iermolenko, Anton Sizov, Eugene Moninets',
    author_email='arturiermolenko@gmail.com, jgenie97@gmail.com, andrii.vynar.om@gmail.com, anatolii.huryk@gmail.com, bigtoxa766@gmail.com',
    description='A CLI telephone book with notes manager.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/payemo/go-it-bot-assistant',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'assistant=go-it-bot-assistant:main',
        ],
    },
)
