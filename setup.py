from setuptools import setup, find_packages

version = open('version').read()

install_requires = [
]

test_require = [
]

dev_require = [
]

setup_args = {
    'name': 'protoc-gen-pydocstring',
    'description': 'Plugin to generate Python docstrings for Google Protobufs.',
    'version': version,
    'python_requires': '>= 3',
    'author': 'Grant Zietsman',
    'author_email': "zietsmangrant@gmail.com",
    'packages': find_packages(include=['protoc_gen_pydocstring*']),
    'install_requires': install_requires,
    'extras_require': {'test': test_require, 'dev': dev_require},
    'package_data': {},
    'package_dir': {'protoc_gen_pydocstring': 'protoc_gen_pydocstring'},
    'scripts': [],
    'entry_points': {
        'console_scripts': [
            'protoc-gen-pydocstring=protoc_gen_pydocstring.main:main',
        ],
    },
}

if __name__ == '__main__':
    setup(**setup_args)
