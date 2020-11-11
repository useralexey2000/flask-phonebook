from setuptools import find_packages, setup

"""
    Setup application
    pip install -e in current dir
"""

setup(
    name='flphone',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click',
        'email-validator',
        'Faker',
        'Flask',
        'Flask-Bcrypt',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Jinja2',
        'setuptools',
        'Werkzeug',
        'WTForms',
    ]
)