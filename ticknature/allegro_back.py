import sys

from ticknature.dominant import dominant
from ticknature.gecko_invest import geckoinvest
from ticknature.instrument_info import instrumentinfo

class AllegroBack():
    def __init__(self):
        pass

    def allegro(self, exch, ins, date_range=[]):
        pass

    def day_trader(self, exch , ins, date, timelist, dir, profit_limit, loss_limit, subject='level1'):
        geckoinvest.day_trader(exch , ins, date, timelist, dir, profit_limit, loss_limit, subject)

    # a$name $exch $ins_type $date1 $date2
    def allegro_special_data(self):
        instruments = dominant.get_instruments(sys.argv[1], sys.argv[2])
        for item_ins in instruments:
            _dates = dominant.get_date(sys.argv[1], item_ins)
            dates = [item for item in _dates if sys.argv[3] <= item <= sys.argv[4]]
            if len(dates) > 0:
                self.allegro(sys.argv[1], item_ins, [dates[0], dates[-1]])

        ret = geckoinvest.get_result(is_save=True)
        print(ret)

    # a$name $exch $ins_type
    def allegro_all_ins(self):
        instruments = dominant.get_instruments(sys.argv[1], sys.argv[2])

        for item_ins in instruments:
            self.allegro(sys.argv[1], item_ins)

        ret = geckoinvest.get_result()
        print(ret)

    # a$name $exch
    def allegro_all_exch(self):
        ins_type_list = instrumentinfo.find_ins(sys.argv[1], 'english')
        for ins_type in ins_type_list:
            instruments = dominant.get_instruments(sys.argv[1], ins_type)
            for item_ins in instruments:
                self.allegro(sys.argv[1], item_ins)

            ret = geckoinvest.get_result()
            print(ret)

    # a$name
    def allegro_all(self):
        print('waitting')

    def run(self):
        if len(sys.argv) == 5:
            self.allegro_special_data()
        elif len(sys.argv) == 3:
            self.allegro_all_ins()
        elif len(sys.argv) == 2:
            self.allegro_all_exch()
        elif len(sys.argv) == 1:
            self.allegro_all()
