from setuptools import setup, find_packages

setup(
    name='ssi_trading',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',  # Example dependency, replace with actual dependencies
        'fastapi',
        'uvicorn',
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'ssi_trading_cli = ssi_trading.cli:main',  # Replace with your CLI entry point
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Your project description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ssi_trading',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
