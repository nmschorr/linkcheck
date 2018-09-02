from setuptools import setup, find_packages

setup(name='linkcheck',
      version='1.2',
      description='Check links from any website',
      author='Nancy Schorr',
      author_email='nancyschorr@yahoo.com',
      packages=find_packages(),
      url='http://schorrmedia.com',
      install_requires=['Flask=1.0.2','requests_html=0.9.0'],
     )