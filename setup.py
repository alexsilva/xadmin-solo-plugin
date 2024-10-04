from setuptools import setup

setup(
    name='xadmin-solo-plugin',
    version='1.1.2',
    packages=['xplugin_solo'],
    url='https://github.com/alexsilva/xadmin-solo-plugin',
    license='MIT',
    author='alex',
    author_email='alex@fabricadigital.com.br',
    description='Site configuration with xadmin',
    install_requires=['django-solo'],
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
    ]
)
