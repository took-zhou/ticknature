from setuptools import find_packages, setup

# 分别读取README.rst和requirements.txt的内容
with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ticknature",
    version="2.6.6",
    author="zhoufan",
    author_email="zhoufan@tsaodai.com",
    description="Nature layer",
    long_description=long_description,
    package_data={"": ["*.csv"]},

    # 项目主页
    url="https://devpi.tsaodai.com",

    # 项目的依赖库，读取的requirements.txt内容
    install_requires=[
        'numpy>=1.23.2', 'statsmodels>=0.13.2', 'pytest>=7.1.2', 'pandas>=1.4.3', 'pandas_market_calendars>=5.1.1', 'setuptools>=39.0.1'
    ],

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages())
