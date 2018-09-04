from setuptools import setup, find_packages

setup(
      name='linkcheck',
      version='1.2',
      description='Check links from any website',
      author='Nancy Schorr',
      author_email='nancyschorr@yahoo.com',
      packages=find_packages(),
      url='http://schorrmedia.com',
      include_package_data=True,
      install_requires=[
            'flask',
            'requests_html',
      ],
      )