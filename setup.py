from setuptools import setup, find_packages

setup(
    author="Gaussian Holdings, LLC",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    description="A tool for retrieving information from EDGAR.",
    name="edgar_data",
    version='0.2.9',
    url='https://github.com/gaussian/edgar-data/',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-mock'],
    install_requires=['requests', 'lxml', 'beautifulsoup4'],
    packages=find_packages()
)
