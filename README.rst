性质层简介
==========

说明
----

tick数据性质分析, 包括原始的性质如最小变动单位, 一手交易单位等浅层性质；也包括相关性，协整性等深层性质

环境搭建
--------

| 为了统一操作环境，将数据映射到interpreter镜像创建的容器中(或是其他容器)，映射路径/home/zhoufan/baidunetdisk:/share/baidunetdisk
| 安装ticknature包：pip install --index-url http://devpi.cdsslh.com:8090/root/dev ticknature --trusted-host devpi.cdsslh.com

功能
----
1手交易单位
^^^^^^^^^^^

python code::

    from ticknature.min_tradeuint import mintradeuint

    # 查找所有合约品种的交易单位
    mintradeuint.find_all()

    # 查找单个合约品种的交易单位
    mintradeuint.find_trade_unit('DCE', 'l2009')
    mintradeuint.find_trade_unit('SHFE', 'cu2009')

最小价格变动单位
^^^^^^^^^^^^^^^^

python code::

    from ticknature.min_ticksize import minticksize

    # 查找所有合约品种的交易单位
    minticksize.find_all()

    # 查找单个合约品种的交易单位
    minticksize.find_tick_size('DCE', 'l2009')
    minticksize.find_tick_size('SHFE', 'cu2009')

最小盈利/亏损变动单位
^^^^^^^^^^^^^^^^^^^^^^^

python code::

    from ticknature.min_tickprice import mintickprice

    # 查找所有合约品种的交易单位
    mintickprice.find_all()

    # 查找单个合约品种的交易单位
    mintickprice.find_tick_price('DCE', 'l2009')
    mintickprice.find_tick_price('SHFE', 'cu2009')

合约交易时间
^^^^^^^^^^^^^

python code::

    # 获取单个合约交易时间表
    from ticknature.trade_time import tradetime
    print(tradetime.get_trade_time('SHFE', 'cu2009'))

输出：{'morning': [[540, 615], [630, 690]], 'afternoon': [[810, 900]], 'night': [[1260, 1440], [0, 60]]}

| [540, 615] 对应上午9点到上午10点15分
| .
| .
| .
| [1260, 1440] 对应晚上9点到晚上12点
| [0, 60] 对应凌晨0点到凌晨1点

python code::

    # 判断某个时刻是否在交易时间内
    from ticknature.trade_time import tradetime
    print(tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 12:10:10'))

输出：False

主力合约判断
^^^^^^^^^^^^^

| 判断持仓量，成交量大约某个阈值的天数占所有交易天数的比重来判断合约是否是主力合约。
| 阈值一共有三个分别为[10000 100000 1000000]

python code::

    from ticknature.dominant import dominant

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

    from ticknature.coint import coint

    coint.paramInput['dataRootPath'] = '/share/baidunetdisk/reconstruct/tick'

    coint.paramInput['instruments1']['exchangeId'] = 'DCE'
    coint.paramInput['instruments1']['instrumentId'] = 'c2105'
    coint.paramInput['instruments2']['exchangeId'] = 'DCE'
    coint.paramInput['instruments2']['instrumentId'] = 'm2105'

    coint.paramInput['duration']['begin'] = '2021-01-01'
    coint.paramInput['duration']['end'] = '2121-03-01'
    result = coint.get_coint()
    print(result)

合约可交易时间点提取
^^^^^^^^^^^^^^^^^^^^^
在拟交易的一天内，逐个读取期货的每笔分时数据，逐个计算每个交易点的价格

python code::

    from ticknature.trade_point import tradepoint
    tradepoint.get_trade_point('SHFE', 'cu2109', '20210329', include_night=True)

基于提取出的交易点，生成相应的峰

python code::

    from ticknature.trade_point import tradepoint
    tradepoint.get_trade_spectrum('SHFE', 'cu2109', '20210329', include_night=True)

合约交易日期提取
^^^^^^^^^^^^^^^^^
获取某个合约的所有交易日期

python code::

    from ticknature.trade_data import tradedata
    tradedata.get_trade_data('DCE', 'c2105')

返回值：['20200716', '20210205', '20210329'...'20210428', '20210426']

交易所包含的合约提取
^^^^^^^^^^^^^^^^^^^^^^

python code::

    from ticknature.trade_data import tradedata
    tradedata.get_instruments('DCE')

返回值：['c2109', 'pg2109', 'pp2201',...'jd2112', 'eb2204']

获取特定品种, 特定月份最新合约名称

python code::

    from ticknature.trade_data import tradedata
    tradedata.get_last_instrument('DCE', 'c2011')

返回值：'c2111'

获取合约是否在交割月

python code::

    from ticknature.trade_data import tradedata
    tradedata.is_delivery_month('DCE', 'c2011')

返回值：False or True

后续功能开发
------------

代码通过git仓库进行管理，下载命令：git clone
ssh://zhoufan@gerrit.cdsslh.com:29418/PY/nature\_analysis -b fen

| 开发模式下安装包： pip install -e 
| 这个命令在部署目录(site-packages)中创建一个指向项目源代码的特殊链接，而不是将整个包复制过去。可以编辑包的源代码而无需重新安装。
