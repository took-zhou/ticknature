import pytest

from ticknature.instrument_info import instrumentinfo


def test_find_ins():
    assert (len(instrumentinfo.find_ins('CZCE')) > 0)
    assert (len(instrumentinfo.find_ins('DCE')) > 0)
    assert (len(instrumentinfo.find_ins('GFEX')) > 0)
    assert (len(instrumentinfo.find_ins('GATE')) > 0)
    assert (len(instrumentinfo.find_ins('SHSE')) > 0)


def test_find_plate():
    assert (len(instrumentinfo.find_plates()) > 0)


def test_find_info():
    assert (instrumentinfo.find_info('GATE', 'BTC_USDT') != '')
    assert (instrumentinfo.find_info('GATE', 'BTI_USDT') == '')


if __name__ == "__main__":
    pytest.main()
