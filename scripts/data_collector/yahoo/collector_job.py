import datetime
from pathlib import Path
import sys

from cfquant.instock.lib import utilsHelper

CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent.parent))

import collector

from dump_bin import DumpDataUpdate,DumpDataAll

dataFolder=f"F:/Project/Gits/ProjectData/qlibdata/"

if utilsHelper.CheckIsHouse() == True:
    dataFolder = f"H:/Stock/ProjectData/qlibdata/"

def update_data_to_bin():
    collector.Run(source_dir=f"{dataFolder}csv",
                  normalize_dir=f'{dataFolder}normalize',
                  max_workers=60).\
        update_data_to_bin(qlib_data_1d_dir=f"{dataFolder}dump",
                                       trading_date="2000-01-01",
                           end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                             delay=0.1)


def dumpAll():
    DumpDataAll(csv_path=f"{dataFolder}normalize",
                  qlib_dir=f'{dataFolder}dump',
                  freq="day",
                   exclude_fields="date,symbol",
                  max_workers=60).dump()


def normalize_data():
    collector.Run(source_dir=f"{dataFolder}csv",
                  normalize_dir=f'{dataFolder}normalize',
                  max_workers=60).normalize_data()

def download_data():
        collector.Run(source_dir=f"{dataFolder}csv",
                      normalize_dir=f'{dataFolder}normalize',
                      max_workers=60).download_data(max_collector_count=60,
                                                    delay=0.1, start="2000-01-01",end=datetime.datetime.now().strftime("%Y-%m-%d"))

if __name__ == '__main__':
    #update_data_to_bin()
    #download_data()
    normalize_data()
    dumpAll()



