from setuptools import setup

setup(
    name='ratatoskr',
    packages=['ratatoskr'],
    include_package_data=True,
    install_requires=[
        'flask',
        'jsonschema',
        'html2text',
        'requests'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'mock'
    ],
)