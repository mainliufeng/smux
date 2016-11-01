from setuptools import setup, find_packages

setup(
    name='command-note',
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
        cmd=command_note.scripts.cmd_command:cmd
    ''',
)
