import datetime
from pathlib import Path
import sys

CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent.parent))

import collector

from dump_bin import DumpDataUpdate

def update_data_to_bin():
    collector.Run(source_dir=f"H:\Stock\ProjectData\qlibdata\csv",
                  normalize_dir=f'H:/Stock/ProjectData/qlibdata/normalize',
                  max_workers=60).\
        update_data_to_bin(qlib_data_1d_dir=f"H:\Stock\ProjectData\qlibdata\dump",
                                       trading_date="2000-01-01",
                           end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                             delay=0.1)


def dumpAll():
    DumpDataUpdate(source_dir=f"H:\Stock\ProjectData\qlibdata\csv",
                  normalize_dir=f'H:/Stock/ProjectData/qlibdata/normalize',
                  max_workers=60).\
        update_data_to_bin(qlib_data_1d_dir=f"H:\Stock\ProjectData\qlibdata\old",
                                       trading_date="2000-01-01",
                           end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                             delay=0.1)

if __name__ == '__main__':
    update_data_to_bin()
