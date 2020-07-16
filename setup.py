from setuptools import setup

setup(
    name='xadmin-solo-plugin',
    version='1.0.0',
    packages=['xplugin_solo'],
    url='https://github.com/alexsilva/xadmin-solo-plugin',
    license='MIT',
    author='alex',
    author_email='alex@fabricadigital.com.br',
    description='Site configuration with xadmin',
    install_requires=['django-solo']
)
