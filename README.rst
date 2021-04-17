性质层简介
==========

说明
----

tick数据性质分析, 包括原始的性质如最小变动单位, 一手交易单位等浅层性质；也包括相关性，协整性等深层性质

环境搭建
--------

| 为了统一操作环境，将数据映射到interpreter镜像创建的容器中(或是其他容器)，映射路径/home/zhoufan/baidunetdisk:/share/baidunetdisk
| 安装nature_analysis包：pip install --index-url http://devpi.cdsslh.com:8090/root/dev nature_analysis --trusted-host devpi.cdsslh.com

功能
----
1手交易单位
^^^^^^^^^^^

python code::

    from nature_analysis.min_tradeuint import mintradeuint

    # 查找所有合约品种的交易单位
    mintradeuint.find_all()

    # 查找单个合约品种的交易单位
    mintradeuint.find_trade_unit('DCE', 'l2009')
    mintradeuint.find_trade_unit('SHFE', 'cu2009')

最小价格变动单位
^^^^^^^^^^^^^^^^

python code::

    from nature_analysis.min_ticksize import minticksize

    # 查找所有合约品种的交易单位
    minticksize.find_all()

    # 查找单个合约品种的交易单位
    minticksize.find_tick_size('DCE', 'l2009')
    minticksize.find_tick_size('SHFE', 'cu2009')

最小盈利/亏损变动单位
^^^^^^^^^^^^^^^^^^^^^^^

python code::

    from nature_analysis.min_tickprice import mintickprice

    # 查找所有合约品种的交易单位
    mintickprice.find_all()

    # 查找单个合约品种的交易单位
    mintickprice.find_tick_price('DCE', 'l2009')
    mintickprice.find_tick_price('SHFE', 'cu2009')

合约交易时间
^^^^^^^^^^^^^

python code::

    # 获取单个合约交易时间表
    from nature_analysis.trade_time import tradetime
    print(tradetime.get_time_list('DCE', 'l2009'))

输出：[[540, 615], [630, 690], [810, 900], [1260, 1500]]

| [540, 615] 对应上午9点到上午10点15分
| .
| .
| .
| [1260, 1500] 对应晚上9点到次日凌晨1点

python code::

    # 判断某个时刻是否在交易时间内
    from nature_analysis.trade_time import tradetime
    print(tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 12:10:10'))

输出：False

主力合约判断
^^^^^^^^^^^^^

| 判断持仓量，成交量大约某个阈值的天数占所有交易天数的比重来判断合约是否是主力合约。
| 阈值一共有三个分别为[10000 100000 1000000]

python code::

    from nature_analysis.dominant import dominant

    dominant.paramInput['dataRootPath'] = '/share/baidunetdisk/reconstruct/tick/DCE/DCE/c2105'
    dominant.paramInput['duration']['begin'] = '2021-01-01'
    dominant.paramInput['duration']['end'] = '2121-03-01'
    result = dominant.genConfidence()
    print(result)

输出：['c2105', 1.0, 1.0, 0.02]

分别代表：

1. 持仓量大于10000&&成交量大于10000占所有天数的比重是百分百，即所有天数都满足
2. 持仓量大于100000&&成交量大于100000占所有天数的比重是百分百，即所有天数都满足
3. 持仓量大于1000000&& 成交量大于1000000占所有天数的比重是百分0.02，即很少天数满足

一般通过判断阈值10000，比重大于百分之五十即可判定是主力合约

合约对协整判断
^^^^^^^^^^^^^^

判断两个合约对是否满足协整检验，采用adfuller算法P

python code::

    from nature_analysis.coint import coint

    coint.paramInput['dataRootPath'] = '/share/baidunetdisk/reconstruct/tick'

    coint.paramInput['instruments1']['exchangeId'] = 'DCE'
    coint.paramInput['instruments1']['instrumentId'] = 'c2105'
    coint.paramInput['instruments2']['exchangeId'] = 'DCE'
    coint.paramInput['instruments2']['instrumentId'] = 'm2105'

    coint.paramInput['duration']['begin'] = '2021-01-01'
    coint.paramInput['duration']['end'] = '2121-03-01'
    result = coint.get_coint()
    print(result)

后续功能开发
------------

代码通过git仓库进行管理，下载命令：git clone
ssh://zhoufan@gerrit.cdsslh.com:29418/PY/nature\_analysis -b fen

| 开发模式下安装包： pip install -e 
| 这个命令在部署目录(site-packages)中创建一个指向项目源代码的特殊链接，而不是将整个包复制过去。可以编辑包的源代码而无需重新安装。
