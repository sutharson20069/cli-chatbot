from setuptools import setup, find_packages

setup(
    name="cli-chatbot",
    version="1.0.0",
    description="A professional CLI chatbot for interviews",
    author="Sutharson",
    author_email="sutharsonmohan@gmail.com",
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'rich>=10.0.0',
        'python-dotenv>=0.19.0',
    ],
    entry_points={
        'console_scripts': [
            'chatbot=chatbot.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)