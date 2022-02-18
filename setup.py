from setuptools import setup, find_packages

# 分别读取README.rst和requirements.txt的内容
with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nature_analysis",
    version="1.1.9",
    author="zhoufan",
    author_email="zhoufan@cdsslh.com",
    description="Nature layer",
    long_description=long_description,

    # 项目主页
    url="http://devpi.cdsslh.com:8090",

    # 项目的依赖库，读取的requirements.txt内容
    install_requires = [
        'numpy>=1.19.1',
        'pytz>=2021.1',
        'statsmodels>=0.12.2',
        'mplfinance>=0.12.7a17',
        'tickmine>=1.0.0'
    ],

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)
