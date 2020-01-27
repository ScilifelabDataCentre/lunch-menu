from setuptools import setup, find_packages

with open(u'requirements.txt') as fp:
    install_requires = list(fp)

setup(
    name='lunch-menu',
    description='Lists current lunch menus at restaurants close to SciLifeLab',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'lunch-menu = lunch_menu.main:main',
        ],
    },
)
