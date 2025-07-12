import pytest

from ticknature.trade_time import tradetime


def test_get_trade_time():
    assert (tradetime.get_trade_time('CZCE')['night_second'] == ['00:00:00', '02:30:00'])
    assert (tradetime.get_trade_time('CZCE', '20250630')['night_second'] == ['2025-06-28 00:00:00', '2025-06-28 02:30:00'])
    assert (tradetime.get_trade_time('GATE')['day_second'] == ['00:00:00', '07:00:00'])
    assert (tradetime.get_trade_time('GATE', '20250627')['day_second'] == ['2025-06-28 00:00:00', '2025-06-28 07:00:00'])
    assert (tradetime.get_trade_time('NASDAQ')['day_second'] == ['00:00:00', '07:00:00'])
    assert (tradetime.get_trade_time('NASDAQ', '20250627')['day_second'] == ['2025-06-28 00:00:00', '2025-06-28 07:00:00'])


def test_get_is_time():
    assert (tradetime.get_is_time('CZCE', '2024-03-01 09:00:00', 'all') == True)
    assert (tradetime.get_is_time('CZCE', '2024-03-01 09:00:00', 'day') == True)
    assert (tradetime.get_is_time('CZCE', '2024-03-01 09:00:00', 'night') == False)
    assert (tradetime.get_is_time('GATE', '2024-03-01 09:00:00') == True)
    assert (tradetime.get_is_time('GATE', '2024-03-01 07:30:00') == False)
    assert (tradetime.get_is_time('NASDAQ', '2024-03-01 21:00:00') == True)
    assert (tradetime.get_is_time('NASDAQ', '2024-03-01 07:30:00') == False)


def test_get_date_time():
    assert (tradetime.get_date_time('CZCE', '20250627', '09:00:00') == '2025-06-27 09:00:00')
    assert (tradetime.get_date_time('CZCE', '20250701', '21:00:00') == '2025-06-30 21:00:00')
    assert (tradetime.get_date_time('GATE', '20250627', '09:00:00') == '2025-06-27 09:00:00')
    assert (tradetime.get_date_time('GATE', '20250627', '06:00:00') == '2025-06-28 06:00:00')
    assert (tradetime.get_date_time('NASDAQ', '20250627', '09:00:00') == '2025-06-27 09:00:00')
    assert (tradetime.get_date_time('NASDAQ', '20250627', '04:00:00') == '2025-06-28 04:00:00')


def test_get_offset_time():
    assert (tradetime.get_offset_time('CZCE', '2025-06-27 09:00:00', -86400) == '2025-06-26 09:00:00')
    assert (tradetime.get_offset_time('CZCE', '2025-07-01 21:00:00', -259200) == '2025-06-28 21:00:00')
    assert (tradetime.get_offset_time('GATE', '2025-06-27 09:00:00', -86400) == '2025-06-26 09:00:00')
    assert (tradetime.get_offset_time('GATE', '2025-06-27 06:00:00', -259200) == '2025-06-24 06:00:00')
    assert (tradetime.get_offset_time('NASDAQ', '2025-06-27 09:00:00', -86400) == '2025-06-26 09:00:00')
    assert (tradetime.get_offset_time('NASDAQ', '2025-06-27 04:00:00', -259200) == '2025-06-24 04:00:00')


if __name__ == "__main__":
    pytest.main()
