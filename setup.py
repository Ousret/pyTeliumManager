from setuptools import setup

setup(
    name='pyTeliumManager',
    version='1.1.0',
    author='Ahmed TAHRI, @Ousret',
    description=('A cross-platform point of sales payment manager tool with Telium Manager '
                 'Support every device with Telium Manager like Ingenico terminals.'),
    license='MIT',
    packages=['telium'],
    test_suite='tests',
    url='https://github.com/Ousret/pyTeliumManager',
    download_url='https://github.com/Ousret/pyAveryBerkel/tarball/1.1.0',
    install_requires=['pyserial', 'pycountry'],
    keywords=['ingenico', 'telium manager', 'telium', 'payment', 'credit card', 'debit card', 'visa', 'mastercard',
              'merchant', 'pos'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)
