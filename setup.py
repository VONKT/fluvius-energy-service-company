from setuptools import setup, find_packages

setup(
    name='fluvius_energy_service_company',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        "PyJWT==2.8.0",
    ],
    author='Ward Schodts',
    author_email='ward@vonkt.energy',
    description='Wrapper for the Fluvius energy service company API that you can use as an "Energie dienstverlener".',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    url='https://github.com/VONKT/fluvius-energy-service-company',
)
