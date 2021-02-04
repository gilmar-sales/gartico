from setuptools import setup

setup(
    name='gartico',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_socketio',
        'mysql-connector-python'
    ],
)