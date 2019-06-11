from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='call-center-simulator',
    version='0.1.0',
    description='Real-time simulator for a sales call center.',
    long_description=readme,
    author='Jack Blandin',
    author_email='jblandin@gohealth.com',
    url='',
    packages=find_packages()
)
