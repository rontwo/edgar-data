from setuptools import setup, find_packages

setup(
    author="Guilherme Caminha",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    description="A tool for retrieving information from SEC.",
    name="sec_retrieval",
    version='0.1.0',
    url='https://github.com/kutakdogan/visor-sec/',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-mock'],
    install_requires=['requests', 'lxml', 'beautifulsoup4'],
    packages=find_packages()
)
