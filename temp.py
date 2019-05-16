#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:32:02 2019

@author: raphael
"""
import csv
from scipy.stats import linregress
import numpy as np


with open('../Data/commenters.csv', 'r') as to_read:
    csvr = csv.reader(to_read)
    header = next(csvr)
    for line in csvr:
        community, snapshot, commenter_count = (int(x) for x in line)
        if not community in metrics_per_com:
            continue
        if not 'nb_commenters' in metrics_per_com[community]:    
            metrics_per_com[community]['nb_commenters'] = []
        metrics_per_com[community]['nb_commenters'].append((snapshot, commenter_count))

class indicators(object):
    
    def slope(self):
        slope_per_com = {}  
        mean_per_com = {}        
        lifetime_per_com = {} 
        for com in metrics_per_com:
            slope_per_com[com] = {}
            mean_per_com[com] = {}
            for indic in metrics_per_com[com]:
                these_indics = metrics_per_com[com][indic]
                x = [x[0] for x in these_indics]
                y = [x[1] for x in these_indics]
                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                slope_per_com[com][indic] = slope
                mean_per_com[com][indic] = np.mean(y)
            lifetime_per_com[com] = len(metrics_per_com[com]['nb_members'])

nb_snapshot_per_community = {}
semantic_metrics = {}
with open('../Results/semantic_metrics.csv', 'r') as to_read:
    csvr = csv.reader(to_read)
    header = next(csvr)
    for line in csvr:
        community = int(line[0])
        snapshot = int(line[1])
        gini = float(line[-1])
        if not community in nb_snapshot_per_community:
            nb_snapshot_per_community[community] = 0
            semantic_metrics[community] = {}
        nb_snapshot_per_community[community] += 1
        semantic_metrics[community][snapshot] = {'gini' : float(gini)}
        
sankey_metrics = {}
with open('../Results/sankey_metrics.csv', 'r') as to_read:
    csvr = csv.reader(to_read)
    header = next(csvr)
    for line in csvr:
        community = int(line[0])
        snapshot = int(line[1])
        if not nb_snapshot_per_community.get(community, 0) > 1:
            continue
        if not community in sankey_metrics:
            sankey_metrics[community] = {snapshot : {}}
        if not snapshot in sankey_metrics[community]:
            sankey_metrics[community][snapshot] = {}
        for i in range(2, len(line)):
            sankey_metrics[community][snapshot][header[i]] = int(line[i])
  
list_indics = ['d_in', 'd_out', 'nb_members']
metrics_per_com = {}          
for com in sankey_metrics:
    metrics_per_com[com] = {}
    for indic in list_indics:
        metrics_per_com[com][indic] = []
        for snapshot in sankey_metrics[com]:
            metrics_per_com[com][indic].append((snapshot, sankey_metrics[com][snapshot][indic]))
        metrics_per_com[com]['gini'] = []
        for snapshot in semantic_metrics[com]:
            metrics_per_com[com]['gini'].append((snapshot, semantic_metrics[com][snapshot]['gini']))
         
for snapshot in range(6): 
    list_edges = []   
    nodes_per_com = {}
    degree_per_vertex = {}
    out_per_vertex = {}
    with open('../Data/edgelists_2019-04-18_102000/edgelist_%s.csv' % snapshot, 'r') as to_read:
        csvr = csv.reader(to_read)
        next(csvr)
        for line in csvr:
            s, v1, v2, com1, com2, ltype = line
            if v1 == v2:
                continue
            if (v1,v2) in list_edges or (v2, v1) in list_edges:
                continue
            list_edges.append((v1,v2))
            com1 = int(com1)
            if not com1 in metrics_per_com:
                continue
            if not com1 in nodes_per_com:
                nodes_per_com[com1] = set()
            if not v1 in degree_per_vertex:
                degree_per_vertex[v1] = 0
            degree_per_vertex[v1] += 1
            if not v1 in out_per_vertex:
                out_per_vertex[v1] = 0
            if ltype == 'out':
                out_per_vertex[v1]  += 1
            nodes_per_com[com1].add(v1)
        
    for community in nodes_per_com:    
        nodes_per_com[community] = list(nodes_per_com[community])
        if not 'odf' in metrics_per_com[community]:
            metrics_per_com[community]['odf'] = []
        
        list_odf = []
        for v in nodes_per_com[community]:
            list_odf.append(out_per_vertex[v] / float(degree_per_vertex[v]))
        metrics_per_com[community]['odf'].append((snapshot, np.mean(list_odf)))
        
 

    
    

list_indics = list_indics + ['gini', 'odf', 'nb_commenters']        
with open('../Results/metrics_per_community.csv', 'w') as to_write:
    csvw = csv.writer(to_write)
    csvw.writerow(['community'] + ['slope_%s' % indic for indic in list_indics] + ['mean_%s' % indic for indic in list_indics] + ['lifetime'])
    for com in metrics_per_com:
        if not 'nb_commenters' in metrics_per_com[com]:
            continue
        csvw.writerow(
                [com] 
                + [slope_per_com[com][indic] for indic in list_indics] 
                + [mean_per_com[com][indic] for indic in list_indics] 
                + [lifetime_per_com[com]]
            )

