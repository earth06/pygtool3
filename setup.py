from setuptools import setup,find_packages

setup(
    name='pygtool3',
    version="0.0.1",
    description="reading gtool3 data",
    long_description="README.md",
    author='Takato Onishi',
    author_email="nnnkjktkt119@gmail.com",
    url="https://github.com/earth06/pygtool3",
    license="info/LICENCE.md",
    install_requires=['numpy','pandas','matplotlib','cartopy','xarray'],
    packages=find_packages(exclude=('test','doc','info'))
)
