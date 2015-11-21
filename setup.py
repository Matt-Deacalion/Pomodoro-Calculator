from setuptools import setup

import pomodoro_calculator

setup(
    name='pomodoro-calculator',
    version=pomodoro_calculator.__version__.strip(),
    url='http://dirtymonkey.co.uk/pomodoro-calculator',
    license='MIT',
    author=pomodoro_calculator.__author__.strip(),
    author_email='matt@dirtymonkey.co.uk',
    description=pomodoro_calculator.__doc__.strip().replace('\n', ' '),
    long_description=open('README.rst').read(),
    keywords='pomodoro productivity timer freelance freelancing',
    packages=['pomodoro_calculator'],
    include_package_data=True,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'get-pomodori = pomodoro_calculator.main:main',
        ],
    },
    install_requires=[
        'colorama>=0.3.1',
        'docopt>=0.6.1',
    ],
    tests_require=[
        'py>=1.4.20',
        'pytest>=2.5.2',
        'freezegun>=0.3.5',
        'python-dateutil>=2.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Utilities',
    ],
)
