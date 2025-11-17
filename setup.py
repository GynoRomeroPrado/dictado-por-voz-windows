"""
Setup script for Dictado por Voz - Windows Desktop App
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='dictado-por-voz-windows',
    version='1.0.0',
    author='Gyno Romero Prado',
    author_email='',
    description='Aplicación de dictado por voz para Windows',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/GynoRomeroPrado/dictado-por-voz-windows',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Win32 (MS Windows)',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'dictado-voz=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'config': ['*.json'],
    },
    keywords='voice dictation speech-to-text windows accessibility',
    project_urls={
        'Bug Reports': 'https://github.com/GynoRomeroPrado/dictado-por-voz-windows/issues',
        'Source': 'https://github.com/GynoRomeroPrado/dictado-por-voz-windows',
    },
)
