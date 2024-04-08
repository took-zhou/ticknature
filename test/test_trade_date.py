import pytest

from ticknature.trade_date import tradedate


def test_get_year():
    assert (tradedate.get_year('CZCE', 'CF501', '20240301') == '2025')
    assert (tradedate.get_year('CZCE', 'CF501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'CF501', '20150121') == '2015')
    assert (tradedate.get_year('SHFE', 'al2501', '20240301') == '2025')
    assert (tradedate.get_year('SHFE', 'al1501', '20150101') == '2015')
    assert (tradedate.get_year('CZCE', 'SA503', '20240320') == '2025')


if __name__ == "__main__":
    pytest.main()
