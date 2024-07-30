import pytest

from ticknature.trade_date import tradedate


def test_get_year():
    assert (tradedate.get_year('CZCE', 'CF501', '20240301') == '2025')
    assert (tradedate.get_year('CZCE', 'CF501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'CF501', '20150121') == '2015')
    assert (tradedate.get_year('SHFE', 'al2501', '20240301') == '2025')
    assert (tradedate.get_year('SHFE', 'al1501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'SA503', '20240320') == '2025')
    assert (tradedate.get_year('INE', 'sc2703', '20240320') == '2027')


def test_get_close_date():
    assert (tradedate.get_close_date('CZCE', 'CF501', '20240301') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'CF501', '20150101') == '20141225')
    assert (tradedate.get_close_date('CZCE', 'CF501', '20150121') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'al2501', '20240301') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'al1501', '20150101') == '20141225')
    assert (tradedate.get_close_date('CZCE', 'SA503', '20240320') == '20250225')
    assert (tradedate.get_close_date('CZCE', 'sc2703', '20240320') == '20270225')


def test_get_prev_date():
    assert (tradedate.get_prev_date('CZCE', '20240410') == '20240409')


if __name__ == "__main__":
    pytest.main()
