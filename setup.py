from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'flask-jwt-extended',
        'python-dotenv',
        'mysql-connector-python',
        'bcrypt'
    ]
) 