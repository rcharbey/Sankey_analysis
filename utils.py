#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:41:16 2019

@author: raphael
"""

import csv

Data = '../Data/'

def is_member_number(line):
    return len(line[2][1].split('.')) == 2

# From old csv format to new in two files
def format_csv(csv_name):
    n_rows, flow_rows = [], []
    with open(Data + csv_name):
        csvr = csv.reader(to_read)
        for line in csvr:
            s = line[1][1]
            community_1 = line[1][0]
            community_2 = line[2][0]
            value = line[3]
            if is_member_number(line):
                n_rows.append([s, community_1, value])