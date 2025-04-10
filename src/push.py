#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 21:43:05 2025

@author: alexandermikhailov
"""


import zipfile
from pathlib import Path

import pandas as pd


def push_to_csv_zip(df: pd.DataFrame, file_path: Path) -> None:
    df.to_csv(file_path, index=True, encoding='utf-8-sig')

    with zipfile.ZipFile(file_path.with_suffix('.zip'), mode='w') as archive:
        archive.write(
            filename=file_path,
            arcname=file_path.name,
            compress_type=zipfile.ZIP_DEFLATED,
        )

    file_path.unlink()
