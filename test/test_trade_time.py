import pytest

from ticknature.trade_time import tradetime


def test_is_trade_time():
    assert (tradetime.is_trade_time('CZCE', 'CF501', '2024-03-01 09:00:00', 'all') == True)
    assert (tradetime.is_trade_time('CZCE', 'CF501', '2024-03-01 09:00:00', 'day') == True)
    assert (tradetime.is_trade_time('CZCE', 'CF501', '2024-03-01 09:00:00', 'night') == False)
    assert (tradetime.is_trade_time('GATE', 'BTC_USDT', '2024-03-01 09:00:00') == True)
    assert (tradetime.is_trade_time('GATE', 'BTC_USDT', '2024-03-01 06:00:00') == False)


if __name__ == "__main__":
    pytest.main()
