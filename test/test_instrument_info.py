import pytest

from ticknature.instrument_info import instrumentinfo


def test_get_exchs():
    assert (len(instrumentinfo.get_exchs()) == 8)


def test_get_exch_type():
    assert (instrumentinfo.get_exch_type("INE") == "future")
    assert (instrumentinfo.get_exch_type("GATE") == "crypto")
    assert (instrumentinfo.get_exch_type("NASDAQ") == "stock")


def test_get_plates():
    assert (len(instrumentinfo.get_plates("")) == 25)


def test_get_groups():
    assert (len(instrumentinfo.get_groups("")) == 2385)


def test_get_ins_exch():
    assert (instrumentinfo.get_ins_exch("TA509") == "CZCE")
    assert (instrumentinfo.get_ins_exch("AAPL") == "NASDAQ")
    assert (instrumentinfo.get_ins_exch("sc2509") == "INE")
    assert (instrumentinfo.get_ins_exch("i2509") == "DCE")
    assert (instrumentinfo.get_ins_exch("TS2508") == "CFFEX")
    assert (instrumentinfo.get_ins_exch("ETH_USDT") == "GATE")
    assert (instrumentinfo.get_ins_exch("1INCH_USDT") == "GATE")
    assert (instrumentinfo.get_ins_exch("A8_USDT") == "GATE")


def test_get_ins_plate():
    assert (instrumentinfo.get_ins_plate("CZCE", "TA509") == "chemical_industry")
    assert (instrumentinfo.get_ins_plate("NASDAQ", "AAPL") == "technology")
    assert (instrumentinfo.get_ins_plate("INE", "sc2509") == "oil")
    assert (instrumentinfo.get_ins_plate("DCE", "i2509") == "black_metals")
    assert (instrumentinfo.get_ins_plate("CFFEX", "TS2508") == "treasury_futures")
    assert (instrumentinfo.get_ins_plate("GATE", "ETH_USDT") == "nodefine")
    assert (instrumentinfo.get_ins_plate("GATE", "1INCH_USDT") == "nodefine")
    assert (instrumentinfo.get_ins_plate("GATE", "A8_USDT") == "nodefine")


def test_get_ins_type():
    assert (instrumentinfo.get_ins_type("CZCE", "TA509") == "TA")
    assert (instrumentinfo.get_ins_type("NASDAQ", "AAPL") == "AAPL")
    assert (instrumentinfo.get_ins_type("INE", "sc2509") == "sc")
    assert (instrumentinfo.get_ins_type("DCE", "i2509") == "i")
    assert (instrumentinfo.get_ins_type("CFFEX", "TS2508") == "TS")
    assert (instrumentinfo.get_ins_type("GATE", "ETH_USDT") == "ETH_USDT")
    assert (instrumentinfo.get_ins_type("GATE", "1INCH_USDT") == "1INCH_USDT")
    assert (instrumentinfo.get_ins_type("GATE", "A8_USDT") == "A8_USDT")


def test_get_ins_group():
    assert (instrumentinfo.get_ins_group("CZCE", "TA509") == "TA09")
    assert (instrumentinfo.get_ins_group("NASDAQ", "AAPL") == "AAPL")
    assert (instrumentinfo.get_ins_group("INE", "sc2509") == "sc09")
    assert (instrumentinfo.get_ins_group("DCE", "i2509") == "i09")
    assert (instrumentinfo.get_ins_group("CFFEX", "TS2508") == "TS08")
    assert (instrumentinfo.get_ins_group("GATE", "ETH_USDT") == "ETH_USDT")
    assert (instrumentinfo.get_ins_group("GATE", "1INCH_USDT") == "1INCH_USDT")
    assert (instrumentinfo.get_ins_group("GATE", "A8_USDT") == "A8_USDT")


def test_get_info():
    assert (len(instrumentinfo.get_ins_info("CZCE", "TA509")) == 8)
    assert (len(instrumentinfo.get_ins_info("NASDAQ", "AAPL")) == 8)
    assert (len(instrumentinfo.get_ins_info("INE", "sc2509")) == 8)
    assert (len(instrumentinfo.get_ins_info("DCE", "i2509")) == 8)
    assert (len(instrumentinfo.get_ins_info("CFFEX", "TS2508")) == 8)
    assert (len(instrumentinfo.get_ins_info("GATE", "ETH_USDT")) == 8)
    assert (len(instrumentinfo.get_ins_info("GATE", "1INCH_USDT")) == 8)
    assert (len(instrumentinfo.get_ins_info("GATE", "A8_USDT")) == 8)


if __name__ == "__main__":
    pytest.main()
