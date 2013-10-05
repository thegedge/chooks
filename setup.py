import chooks

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='chooks',
    version=chooks.__version__,
    scripts=['bin/chooks'],
    packages=[
        'chooks',
        'chooks.commands',
    ],

    install_requires=['docopt==0.6.1'],
    package_data={'': ['README.md', 'LICENSE']},
    include_package_data=True,
    zip_safe=True,

    # PyPi Metadata
    author='Jason Gedge',
    author_email='',
    url='http://github.com/thegedge/chooks',
    description='Easily customizable git hooks',
    long_description=open('README.md').read(),
    license='MIT',
    keywords='git hooks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities',
    ],
)
