#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:41:16 2019

@author: raphael
"""

import csv

Data = '../Data/'

class formating_data(object):
    def __init__(self, filename):
        self.filename = filename
        self.n_rows = []
        self.flow_rows = []

    def is_member_number(self, line):
        return line[2].strip('()').split(',')[1][-2:] == '.1'
    
    # From old csv format to new in two files
    def read_csv(self):
        with open(Data + self.filename + '.csv') as to_read:
            csvr = csv.reader(to_read)
            next(csvr)
            for line in csvr:
                s = line[1].strip('()').split(',')[1]
                community_1 = line[1].strip('()').split(',')[0]
                community_2 = line[2].strip('()').split(',')[0]
                value = int(line[3])
                if self.is_member_number(line):
                    self.n_rows.append([s, community_1, value])
                else:
                    s = s.split('.')[0]
                    self.flow_rows.append([s, community_1, community_2, value])
                
    def write_data(self):
        with open(Data + self.filename + '_nb_members_per_community.csv', 'w') as to_write:
            csvw = csv.writer(to_write)
            csvw.writerow(['snapshot', 'community', 'nb_members'])
            for row in self.n_rows:
                csvw.writerow(row)
                
        
        with open(Data + self.filename + '_flows.csv', 'w') as to_write:
            csvw = csv.writer(to_write)
            csvw.writerow(['snapshot', 'community_1', 'community_2', 'weight'])
            for row in self.flow_rows:
                csvw.writerow(row)
                
    def run(self):
        self.read_csv()
        self.write_data()