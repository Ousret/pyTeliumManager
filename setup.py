from setuptools import setup
import io
import os

from re import search


def get_version():
    with open('telium/version.py') as version_file:
        return search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                      version_file.read()).group('version')


here = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = ('A cross-platform point of sales payment manager tool with Telium Manager '
               'Support every device with Telium Manager like Ingenico terminals.')

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name='pyTeliumManager',
    version=get_version(),
    author='Ahmed TAHRI, @Ousret',
    author_email='ahmed.tahri@cloudnursery.dev',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['telium'],
    test_suite='test',
    url='https://github.com/Ousret/pyTeliumManager',
    install_requires=[
        'pyserial>=3.3',
        'pycountry>=17.0,<18.5.20',
        'payment_card_identifier>=0.1.2',
        'six'
    ],
    tests_require=['Faker', 'pytest'],
    keywords=['ingenico', 'telium manager', 'telium', 'payment', 'credit card', 'debit card', 'visa', 'mastercard',
              'merchant', 'pos'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
