#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 23:51:24 2022

@author: Alexander Mikhailov
"""


import pandas as pd

from config import DATA_DIR, FILE_NAME
from push import push_to_csv_zip
from transform import insert_desc_and_swap_cols


def main() -> None:
    file_path = DATA_DIR.joinpath(FILE_NAME)

    pd.concat(
        [
            pd.read_csv(name, index_col=0).pipe(insert_desc_and_swap_cols)
            for name in DATA_DIR.iterdir()
        ]
    ).pipe(push_to_csv_zip, file_path)


if __name__ == '__main__':
    main()
