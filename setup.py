from setuptools import setup
# from distutils.extension import Extension

"""
from Cython.Build import cythonize

extensions = [
    Extension("__init__", ["telium/__init__.py"]),
    Extension("constant", ["telium/constant.py"]),
    Extension("payment", ["telium/payment.py"]),
    Extension("manager", ["telium/telium.py"])
]
"""

setup(
    name='pyTeliumManager',
    version='2.0.2',
    author='Ahmed TAHRI, @Ousret',
    author_email='ahmed@tahri.space',
    description=('A cross-platform point of sales payment manager tool with Telium Manager '
                 'Support every device with Telium Manager like Ingenico terminals.'),
    license='MIT',
    packages=['telium'],
    test_suite='tests',
    url='https://github.com/Ousret/pyTeliumManager',
    download_url='https://github.com/Ousret/pyTeliumManager/archive/2.0.2.tar.gz',
    install_requires=['pyserial', 'pycountry>=17.0'],
    keywords=['ingenico', 'telium manager', 'telium', 'payment', 'credit card', 'debit card', 'visa', 'mastercard',
              'merchant', 'pos'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # ext_modules=cythonize(extensions)
)
