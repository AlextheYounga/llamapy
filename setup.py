from setuptools import setup, find_packages

setup(
    name='local-llm-api',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A local API for LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/local-llm-api',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'requests',
		'fake-useragent',
		'aiohttp',
		'fastapi'
    ],
)