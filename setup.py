from setuptools import find_packages, setup
setup(
    name='hyperparamlib',
    packages=find_packages(include=['hyperparamlib']),
    version='0.1.0',
    description='Expore hyperparam space',
    author='Me',
    license='MIT',
    test_suite='tests',
)