
from __future__ import absolute_import, print_function

requires = [
    "requests>=2.5.0"
]

config = {
    'name': 'dcsh',
    'version': '0.0.1',
    'description': 'execute scripts anywhere on your mesos cluster',
    'author': 'Thomas Rampelberg',
    'author_email': 'thomas@mesosphere.io',

    'packages': [
        'dcsh'
    ],
    'entry_points': {
        'console_scripts': [
            'dcsh = dcsh.main:main',
        ]
    },
    'setup_requires': [ ],
    'install_requires': requires,
    'dependency_links': [ ],
    'tests_require': [ ],
    'scripts': [ ]
}

if __name__ == "__main__":
    from setuptools import setup

    setup(**config)
