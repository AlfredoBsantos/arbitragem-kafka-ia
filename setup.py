from setuptools import setup, find_packages

setup(
    name="arbitragem_kafka_ia",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'web3',
        'kafka-python',
        'python-dotenv'
    ],
)