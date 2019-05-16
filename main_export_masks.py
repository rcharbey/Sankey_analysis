#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:03:42 2019

@author: raphael
"""

from PMGraph import PMGraph
import csv
    
pmg = PMGraph.read('../Data/edgescommunities')
with open('../Results/sankey_metrics.csv', 'w') as to_write:
    csvw = csv.writer(to_write)
    header = ['community', 'snapshot', 'd_in', 'd_out', 'nb_members']
    csvw.writerow(header)
    for i in pmg.temporal_communities:
        tc = pmg.temporal_communities[i]
        list_sankey_metrics = tc.export_evolution()
        for sankey_metrics in list_sankey_metrics:
            csvw.writerow(sankey_metrics)