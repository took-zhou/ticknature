import pytest

from ticknature.trade_date import tradedate


def test_get_tick_date():
    assert (tradedate.get_tick_date('CZCE', '2025-06-27 15:00:00') == '20250627')
    assert (tradedate.get_tick_date('CZCE', '2025-06-27 21:00:00') == '20250630')
    assert (tradedate.get_tick_date('INE', '2025-06-27 15:00:00') == '20250627')
    assert (tradedate.get_tick_date('INE', '2025-06-27 21:00:00') == '20250630')
    assert (tradedate.get_tick_date('GATE', '2025-06-27 06:00:00') == '20250626')
    assert (tradedate.get_tick_date('GATE', '2025-06-27 08:00:00') == '20250627')
    assert (tradedate.get_tick_date('NASDAQ', '2025-06-27 05:00:00') == '20250626')
    assert (tradedate.get_tick_date('NASDAQ', '2025-06-27 21:00:00') == '20250627')


def test_get_trade_dates():
    assert (len(tradedate.get_trade_dates('CZCE')) > 100)
    assert (len(tradedate.get_trade_dates('GATE')) > 100)
    # assert (len(tradedate.get_trade_dates('NASDAQ')) > 100)


def test_get_prev_date():
    assert (tradedate.get_prev_date('CZCE', '20250627') == '20250626')
    assert (tradedate.get_prev_date('CZCE', '20250623') == '20250620')
    assert (tradedate.get_prev_date('INE', '20250627') == '20250626')
    assert (tradedate.get_prev_date('INE', '20250623') == '20250620')
    assert (tradedate.get_prev_date('GATE', '20250626') == '20250625')
    assert (tradedate.get_prev_date('GATE', '20250627') == '20250626')
    #assert (tradedate.get_prev_date('NASDAQ', '20250626') == '20250625')
    #assert (tradedate.get_prev_date('NASDAQ', '20250627') == '20250626')


def test_get_after_date():
    assert (tradedate.get_after_date('CZCE', '20250626') == '20250627')
    assert (tradedate.get_after_date('CZCE', '20250620') == '20250623')
    assert (tradedate.get_after_date('INE', '20250626') == '20250627')
    assert (tradedate.get_after_date('INE', '20250620') == '20250623')
    assert (tradedate.get_after_date('GATE', '20250625') == '20250626')
    assert (tradedate.get_after_date('GATE', '20250626') == '20250627')
    #assert (tradedate.get_after_date('NASDAQ', '20250625') == '20250626')
    #assert (tradedate.get_after_date('NASDAQ', '20250626') == '20250627')


def test_get_close_date():
    assert (tradedate.get_close_date('CZCE', 'CF501', '20240301') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'CF501', '20150101') == '20141225')
    assert (tradedate.get_close_date('CZCE', 'CF501', '20150121') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'al2501', '20240301') == '20241225')
    assert (tradedate.get_close_date('CZCE', 'al1501', '20150101') == '20141225')
    assert (tradedate.get_close_date('CZCE', 'SA503', '20240320') == '20250225')
    assert (tradedate.get_close_date('CZCE', 'sc2703', '20240320') == '20270225')
    assert (tradedate.get_close_date('GATE', '1INCH_USDT', '20240320') == '21001225')
    assert (tradedate.get_close_date('GATE', 'A8_USDT', '20240320') == '21001225')
    assert (tradedate.get_close_date('NASDAQ', 'AAPL', '20240320') == '21001225')
    assert (tradedate.get_close_date('NASDAQ', 'NVDA', '20240320') == '21001225')


def test_get_delivery_date():
    assert (tradedate.get_delivery_date('CZCE', 'CF501', '20240301') == '20250115')
    assert (tradedate.get_delivery_date('CZCE', 'CF501', '20150101') == '20150115')
    assert (tradedate.get_delivery_date('CZCE', 'CF501', '20150121') == '20250115')
    assert (tradedate.get_delivery_date('CZCE', 'al2501', '20240301') == '20250115')
    assert (tradedate.get_delivery_date('CZCE', 'al1501', '20150101') == '20150115')
    assert (tradedate.get_delivery_date('CZCE', 'SA503', '20240320') == '20250315')
    assert (tradedate.get_delivery_date('CZCE', 'sc2703', '20240320') == '20270315')
    assert (tradedate.get_delivery_date('GATE', '1INCH_USDT', '20240320') == '21001231')
    assert (tradedate.get_delivery_date('GATE', 'A8_USDT', '20240320') == '21001231')
    assert (tradedate.get_delivery_date('NASDAQ', 'AAPL', '20240320') == '21001231')
    assert (tradedate.get_delivery_date('NASDAQ', 'NVDA', '20240320') == '21001231')


def test_get_year():
    assert (tradedate.get_year('CZCE', 'CF501', '20240301') == '2025')
    assert (tradedate.get_year('CZCE', 'CF501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'CF501', '20150121') == '2015')
    assert (tradedate.get_year('SHFE', 'al2501', '20240301') == '2025')
    assert (tradedate.get_year('SHFE', 'al1501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'SA503', '20240320') == '2025')
    assert (tradedate.get_year('INE', 'sc2703', '20240320') == '2027')


def test_get_login_date():
    assert (tradedate.get_login_date('2025-06-27 20:05:00') == '20250630')
    assert (tradedate.get_login_date('2025-06-27 15:00:00') == '20250627')
    assert (tradedate.get_login_date('2025-06-27 20:35:00') == '20250627')
    assert (tradedate.get_login_date('2025-06-27 05:00:00') == '20250626')
    assert (tradedate.get_login_date('2025-06-27 07:00:00') == '20250626')
    assert (tradedate.get_login_date('2025-06-27 08:00:00') == '20250627')


if __name__ == "__main__":
    pytest.main()
