from setuptools import setup, find_packages

setup(
    name='Global-Data-Interface',
    version='0.1.0a1',
    description='Global Data Interface is a Python package designed to provide a unified interface to easily query for data from a number of APIs providing international time series data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Euan McLean Campbell',
    author_email='euan.campbell.dev@pm.me',
    url='https://github.com/EMCampbell01/Global-Data-Interface',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[  
        'Requests==2.32.3',
        'setuptools==65.5.0',
    ],
)