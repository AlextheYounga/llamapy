from setuptools import setup, find_packages

setup(
    name='llamapy',
    version='0.1.0',
    author='Alex Younger',
    author_email='thealexyounger@proton.me',
    description='A local API for LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlextheYounga/llamapy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
		'requests'
		'gputil'
		'openai'
		'tqdm'
    ],
)