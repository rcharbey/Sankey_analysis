#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 17:44:39 2019

@author: raphael
"""
import csv
from datetime import datetime

snapshot_boundaries = [1448262488, 1449590600, 1450909539, 1452222043, 1453542221, 1454860444, 1456185600]

def find_snapshot(date):
    """
        Give the snapshot id corresponding to a line
        Require snapshot_values and snapshot_boundaries as global variable
        :param: dataframe row with a column nammed 'timestamp'
        :return: snapshot correspond to the timestamp in the row
    """
    for i, begin in enumerate(snapshot_boundaries):
        if begin > date:
            return i-1
        
name_to_id, id_to_name = {}, {}

thread_per_timestamp = {}
with open('../../anr-pil/network/data/Database/comments.csv') as to_read:
    csvr = csv.reader(to_read)
    next(csvr)
    for line in csvr:
        author = line[3]
        timestamp = line[5]
        timestamp_temp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000Z').timestamp()
        thread = line[7]
        timestamp_formatted = int(timestamp_temp) 
        if line[0] == 'UgitUpltft-vjHgCoAEC.85XXvn30nsA88BbWFIcY-A':
            print(timestamp_temp)
            print(timestamp_formatted)
            print(line)
            
        if timestamp_formatted == 1451058478:
            print(line)
        thread_per_timestamp[timestamp_formatted] = thread        
       
with open('../Data/Active_network_base/authorsname_nodeid.csv', 'r') as to_read:
    csvr = csv.reader(to_read, delimiter = ' ')
    header = next(csvr)
    for line in csvr:
        name_to_id[line[0]] = line[1]
        id_to_name[line[1]] = line[0]
        
former_snap = -1

with open('../Data/tedgelist_2019-04-06T220300/tedgelist_20151123_20160203.ncol', 'r') as to_read:
    csvr = csv.reader(to_read, delimiter = ' ')
    next(csvr)
    for line in csvr:
        comment_id = line[3]
        if 'UgitUpltft-vjHgCoAEC' in line[3] or 'UgitUpltft-vjHgCoAEC' in line[4]:
            snapshot = find_snapshot(int(line[0]))
            if snapshot == 6:
                continue
            if snapshot > former_snap:
                print()
                former_snap = snapshot
            #print('%s %s %s %s' % (snapshot, name_to_id[line[1]], name_to_id[line[2]], thread_per_timestamp[int(line[0])]))
            print('%s %s %s %s' % (snapshot, name_to_id[line[1]], name_to_id[line[2]], comment_id))