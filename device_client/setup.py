from setuptools import setup, find_packages

setup(
    name='device_client',
    version='0.0.1',
    packages=['device_client'],
    install_requires=[
        'paho-mqtt==1.3.1'
    ]
)
