from setuptools import setup, find_packages

setup(
      name='LinkCheck',
      version='1.4',
      description='Check links from any website',
      author='Nancy Schorr',
      author_email='nancyschorr@yahoo.com',
      packages=find_packages(),
      #url='http://linkcheckpy-linkcheckpy.7e14.starter-us-west-2.openshiftapps.com',
      include_package_data=True,
      install_requires=[
            'flask',
            'requests_html',
            'validators',
            'jinja2',
            'waitress',
            'requests',
      ],
      )