#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 21:44:36 2025

@author: alexandermikhailov
"""


import pandas as pd


def insert_desc_and_swap_cols(df: pd.DataFrame) -> pd.DataFrame:
    desc_value = df.columns[-1]
    df.insert(loc=1, column='desc', value=desc_value)
    df.columns = ['value', 'desc']
    return df[df.columns[::-1]]
