import pytest

from ticknature.instrument_info import instrumentinfo
from tickmine.api import get_ins, get_kline


def test_get_exchs():
    assert (len(instrumentinfo.get_exchs()) == 10)


def test_get_exch_type():
    assert (instrumentinfo.get_exch_type("INE") == "future")
    assert (instrumentinfo.get_exch_type("GATE") == "crypto")
    assert (instrumentinfo.get_exch_type("NASDAQ") == "stock")


def test_get_plates():
    assert (len(instrumentinfo.get_plates("")) == 26)


def test_get_groups():
    assert (len(instrumentinfo.get_groups("")) == 3524)


def test_get_ins_exch():
    assert (instrumentinfo.get_ins_exch("TA509") == "CZCE")
    assert (instrumentinfo.get_ins_exch("AAPL") == "NASDAQ")
    assert (instrumentinfo.get_ins_exch("sc2509") == "INE")
    assert (instrumentinfo.get_ins_exch("i2509") == "DCE")
    assert (instrumentinfo.get_ins_exch("TS2508") == "CFFEX")
    assert (instrumentinfo.get_ins_exch("ETH_USDT") == "GATE")
    assert (instrumentinfo.get_ins_exch("BTC_USDT") == "GATE")
    assert (instrumentinfo.get_ins_exch("FORM_USDT") == "GATE")


def test_get_ins_plate():
    assert (instrumentinfo.get_ins_plate("CZCE", "TA509") == "energy&chemicals")
    assert (instrumentinfo.get_ins_plate("NASDAQ", "AAPL") == "technology")
    assert (instrumentinfo.get_ins_plate("INE", "sc2509") == "energy&chemicals")
    assert (instrumentinfo.get_ins_plate("DCE", "i2509") == "ferrous_metals")
    assert (instrumentinfo.get_ins_plate("CFFEX", "TS2508") == "financials")
    assert (instrumentinfo.get_ins_plate("GATE", "ETH_USDT") == "nodefine")
    assert (instrumentinfo.get_ins_plate("GATE", "BTC_USDT") == "nodefine")
    assert (instrumentinfo.get_ins_plate("GATE", "FORM_USDT") == "nodefine")


def test_get_ins_type():
    assert (instrumentinfo.get_ins_type("CZCE", "TA509") == "TA")
    assert (instrumentinfo.get_ins_type("NASDAQ", "AAPL") == "AAPL")
    assert (instrumentinfo.get_ins_type("INE", "sc2509") == "sc")
    assert (instrumentinfo.get_ins_type("DCE", "i2509") == "i")
    assert (instrumentinfo.get_ins_type("CFFEX", "TS2508") == "TS")
    assert (instrumentinfo.get_ins_type("GATE", "ETH_USDT") == "ETH_USDT")
    assert (instrumentinfo.get_ins_type("GATE", "BTC_USDT") == "BTC_USDT")
    assert (instrumentinfo.get_ins_type("GATE", "FORM_USDT") == "FORM_USDT")


def test_get_ins_group():
    assert (instrumentinfo.get_ins_group("CZCE", "TA509") == "TA09")
    assert (instrumentinfo.get_ins_group("NASDAQ", "AAPL") == "AAPL")
    assert (instrumentinfo.get_ins_group("INE", "sc2509") == "sc09")
    assert (instrumentinfo.get_ins_group("DCE", "i2509") == "i09")
    assert (instrumentinfo.get_ins_group("CFFEX", "TS2508") == "TS08")
    assert (instrumentinfo.get_ins_group("GATE", "ETH_USDT") == "ETH_USDT")
    assert (instrumentinfo.get_ins_group("GATE", "BTC_USDT") == "BTC_USDT")
    assert (instrumentinfo.get_ins_group("GATE", "FORM_USDT") == "FORM_USDT")


def test_get_info():
    assert (len(instrumentinfo.get_ins_info("CZCE", "TA509")) == 9)
    assert (len(instrumentinfo.get_ins_info("NASDAQ", "AAPL")) == 9)
    assert (len(instrumentinfo.get_ins_info("INE", "sc2509")) == 9)
    assert (len(instrumentinfo.get_ins_info("DCE", "i2509")) == 9)
    assert (len(instrumentinfo.get_ins_info("CFFEX", "TS2508")) == 9)
    assert (len(instrumentinfo.get_ins_info("GATE", "ETH_USDT")) == 9)
    assert (len(instrumentinfo.get_ins_info("GATE", "BTC_USDT")) == 9)
    assert (len(instrumentinfo.get_ins_info("GATE", "FORM_USDT")) == 9)


def test_market_cap_rank():
    exch_list = ['SEHK', 'NASDAQ', 'GATE']
    for exch in exch_list:
        test_date = '20200702'
        ins_list = get_ins(exch, special_date=test_date)
        market_cap_dict = {}
        for ins in ins_list:
            d_kline = get_kline(exch, ins, test_date, period='1D')
            if len(d_kline) == 0:
                continue
            ins_info = instrumentinfo.get_ins_info(exch, ins)
            if 'shares' not in ins_info:
                continue
            shares = ins_info['shares']
            d_share = shares[0]['value']
            for share in shares[1:]:
                if test_date <= share['date']:
                    d_share = share['value']
                    break
            market_cap = d_kline.Close[0] * d_share
            market_cap_dict[ins] = market_cap
        market_cap_sorted = sorted(market_cap_dict.items(), key=lambda x: x[1], reverse=True)
        if exch == 'SEHK':
            assert (market_cap_sorted[0][0] == '700')
            assert (market_cap_sorted[1][0] == '9988')
            assert (market_cap_sorted[2][0] == '939')
        elif exch == 'NASDAQ':
            assert (market_cap_sorted[0][0] == 'AMZN')
            assert (market_cap_sorted[1][0] == 'MSFT')
            assert (market_cap_sorted[2][0] == 'AAPL')
        elif exch == 'GATE':
            assert (market_cap_sorted[0][0] == 'BTC_USDT')
            assert (market_cap_sorted[1][0] == 'ETH_USDT')
            assert (market_cap_sorted[2][0] == 'XRP_USDT')

        test_date = '20250702'
        ins_list = get_ins(exch, special_date=test_date)
        for ins in ins_list:
            d_kline = get_kline(exch, ins, test_date, period='1D')
            if len(d_kline) == 0:
                continue
            ins_info = instrumentinfo.get_ins_info(exch, ins)
            if 'shares' not in ins_info:
                continue
            shares = ins_info['shares']
            d_share = shares[0]['value']
            for share in shares[1:]:
                if test_date <= share['date']:
                    d_share = share['value']
                    break
            market_cap = d_kline.Close[0] * d_share
            market_cap_dict[ins] = market_cap
        market_cap_sorted = sorted(market_cap_dict.items(), key=lambda x: x[1], reverse=True)
        if exch == 'SEHK':
            assert (market_cap_sorted[0][0] == '700')
            assert (market_cap_sorted[1][0] == '9988')
            assert (market_cap_sorted[2][0] == '939')
        elif exch == 'NASDAQ':
            assert (market_cap_sorted[0][0] == 'NVDA')
            assert (market_cap_sorted[1][0] == 'MSFT')
            assert (market_cap_sorted[2][0] == 'AAPL')
        elif exch == 'GATE':
            assert (market_cap_sorted[0][0] == 'BTC_USDT')
            assert (market_cap_sorted[1][0] == 'ETH_USDT')
            assert (market_cap_sorted[2][0] == 'XRP_USDT')


if __name__ == "__main__":
    # python test_instrument_info.py -k "test_market_cap_rank"
    pytest.main()
