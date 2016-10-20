from setuptools import setup

setup(
    name='pyTeliumManager',
    version='1.0.0',
    author='SARL Distrigel',
    description=('A cross-platform communication tool for Avery Berkel Scales '
                 'Create, modify, delete and get PLU from any Berkel Scale'),
    license='MIT',
    packages=['TeliumManager'],
    test_suite='tests',
    install_requires=['pyserial', 'pycountry'],
    keywords="telium manager tpe ingenico usb com iwl250",
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