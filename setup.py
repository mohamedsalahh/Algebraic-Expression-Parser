"""Setup logic for pip."""

from setuptools import setup


setup(
    name='Algebraic-Expression-Parser',
    version='0.0.2',
    DESCRIPTION = 'Algebraic Expression Parser',
    LONG_DESCRIPTION = 'Control and handle any algebraic expression, as well as do common expression operations such as getting postfix, prefix, and expression tree.',
    url='https://github.com/mohamedsalahh/Algebraic-Expression-Parser',
    author='Mohamed Salah',
    author_email='mohamed.s636499@gmail.com',
    license='MIT',
    keywords='Algebraic Expression Parser',
    install_requires=[
          'binarytree',
      ],
)
