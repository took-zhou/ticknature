import pytest

def test_active():
    from ticknature.active import activefuture

    ret = activefuture.get('CZCE', 'MA201')
    assert(ret[2]>0.5)
    assert(ret[3]>0.3)
    assert(ret[4]>0.1)
    ret = activefuture.get_date('CZCE', 'MA201')
    assert(len(ret) > 10)

def test_coint():
    from ticknature.coint import cointfuture

    ret = cointfuture.get_pair_data('CZCE', 'MA201', 'CZCE', 'MA205', ['20211101', '20211130'])
    assert(len(ret) > 10)
    ret = cointfuture.get_coint(ret)
    assert(ret[0]<-2.5)

def test_dominant():
    from ticknature.dominant import dominant

    ret = dominant.get_date('CZCE', 'TA205')
    assert(len(ret)>10)
    ret = dominant.get_instruments('CZCE', 'TA')
    assert(len(ret)>10)
    ret = dominant.get_newest_instrument('CZCE', 'TA')
    assert(ret=='TA209')
    ret = dominant.get_newest_instrument('CZCE', 'TA209')
    assert(ret!='')

def test_instrument_info():
    from ticknature.instrument_info import instrumentinfo

    ret = instrumentinfo.find_chinese_name('CZCE', 'MA205')
    assert(ret=='甲醇')
    ret = instrumentinfo.find_exch('MA205')
    assert(ret=='CZCE')
    ret = instrumentinfo.find_ins('CZCE')
    assert(len(ret)>=10)
    ret = instrumentinfo.find_ins_type('CZCE', 'MA205')
    assert(ret=='MA')

def test_trade_date():
    from ticknature.trade_date import tradedate
    ret = tradedate.get_tick_date('2022-04-04 09:00:00.500')
    assert(ret=='20220404')

    ret = tradedate.get_tick_date('2022-04-04 21:00:00.500')
    assert(ret=='20220405')

    ret = tradedate.get_tick_date('2022-04-05 01:00:00.500')
    assert(ret=='20220405')

    ret = tradedate.get_tick_date('2022-04-08 21:00:00.500')
    assert(ret=='20220411')

    ret = tradedate.get_tick_date('2022-04-09 02:00:00.500')
    assert(ret=='20220411')

def test_min():
    from ticknature.min_commission import mincommission
    from ticknature.min_deposit import mindeposit
    from ticknature.min_tickprice import mintickprice
    from ticknature.min_ticksize import minticksize
    from ticknature.min_tradeuint import mintradeuint

if __name__ =="__main__":
    pytest.main()
