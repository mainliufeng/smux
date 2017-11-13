from setuptools import setup, find_packages

setup(
    name='smux',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'prettytable',
        'fuzzywuzzy'
    ],
    entry_points='''
        [console_scripts]
        smux=smux.scripts.cmd_smux:smux
    ''',
)
