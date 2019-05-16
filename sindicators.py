#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:28:01 2019

@author: raphael
"""

from snapshot_graph import Sgraph
from scipy.stats import linregress
import csv
import itertools

class utils(object):
    def __init__(self, values):
        self.values = values
    
    def gini(self):
        if not self.values:
                return '_'
        sorted_list = sorted(self.values)
        height, area = 0, 0
        for value in sorted_list:
            height += value
            area += height - value / 2.
        fair_area = height * len(self.values) / 2.
        if fair_area == 0:
            return -1
        return (fair_area - area) / fair_area
            
    
    def slope(self):
        x = [x for x in self.values.values()]
        y = [y for y in self.values.keys()]
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        return slope
    
    def mean(self):
        values = [v for v in self.values.values() if not v == -1]
        if len(values) == 0:
            return -1
        return sum(values)/float(len(values))


class SG_vertex_indicators(object):
    def __init__(self, svertex):
        self.svertex = svertex
         
    def out_degree(self, active = False):
        adjacent_edges = self.svertex.get_adjacent_edges(active)
        return len([se for se in adjacent_edges if se.sv1.community.id != se.sv2.community.id])
        
    def IDF(self, active = False):
        out_degree = self.out_degree(active) 
        degree = self.svertex.degree(active)
        if degree == 0:
            return 1
        return (degree - out_degree) / float(degree)    
        
        
        
class SG_community_indicators(object):
    def __init__(self, community):
        self.community = community
    
    def out_degree_distribution(self, active = False):
        result = []
        for svertex in self.community.members:
            result.append(SG_vertex_indicators(svertex).out_degree(active))
        return result
    
    def meanIDF(self, active):
        sum_IDF = 0
        _vertices = self.community.members if not active else self.community.get_active_members()
        _nb_members = self.community.nb_members if not active else self.community.nb_active_members
        for svertex in _vertices:
            sum_IDF += SG_vertex_indicators(svertex).IDF(active)   
        try:             
            return sum_IDF / float(_nb_members)
        except:
            return 1
    
    def ratio_active_members(self):
        nb_active_vertices = len([v for v in self.community.members if v.is_active])
        return nb_active_vertices / float(self.community.nb_members)
    
    def nb_messages(self):
        return [svertex.nb_messages for svertex in self.community.members]
    
    def nb_common_threads(self, active = False):
        sum_common_threads = 0
        for sv1, sv2 in itertools.combinations(self.community.members, 2):
            if not sv1.is_neighbor(sv2):
                continue
            sum_common_threads += sv1.number_co_active_threads(sv2)
        return sum_common_threads / float(self.community.nb_members)
            
    

class SG_Indicators(object):
    
    def __init__(self, sgraph):
        self.sgraph = sgraph
        
    def out_ties_per_community_members(self, active = False):
        result = {}
        for community in self.sgraph.get_communities():
            com_indics = SG_community_indicators(community)
            u = utils(com_indics.out_degree_distribution(active))
            result[community.id] = u.gini()
        return result
            
    def meanIDF(self, active = False):
        result = {}
        for community in self.sgraph.get_communities():
            result[community.id] = SG_community_indicators(community).meanIDF(active)

        return result
    
    def ratio_active_members(self):
        result = {}
        for community in self.sgraph.get_communities():
            result[community.id] = SG_community_indicators(community).ratio_active_members()
        
        return result
    
    def nb_messages(self):
        result = {}
        for community in self.sgraph.get_communities():
            result[community.id] = sum(SG_community_indicators(community).nb_messages())
        
        return result
    
    def nb_members(self):
        result = {}
        for community in self.sgraph.get_communities():
            nb_vertices = len([v for v in self.sgraph.vs if v.community == community])
            result[community.id] = nb_vertices
        
        return result
    
    def nb_common_threads(self, active = False):
        result = {}
        for community in self.sgraph.get_communities():
            nb_vertices = len([v for v in self.sgraph.vs if v.community == community])
            result[community.id] = nb_vertices
        
        return result    


def fusion(dic1, dic2, snapshot, name):
    for community in dic2:
        if not community in dic1:
            dic1[community] = {name : {}}
        if not name in dic1[community]:
            dic1[community][name] = {}
        dic1[community][name][snapshot] = dic2[community]
    return dic1
    
results = {}    
for i in range(6):   
    print('snapshot %s' % i)
    sg = Sgraph.from_base('../Data/Active_network_base/build_active_network_base_v43.csv', i)
    sg.to_print()

    ind = SG_Indicators(sg)
    results = fusion(results, ind.nb_messages(), i, 'nb_messages')
    results = fusion(results, ind.nb_common_threads(active = True), i, 'nb_common_threads_active')
    results = fusion(results, ind.nb_common_threads(), i, 'nb_common_threads')
    results = fusion(results, ind.meanIDF(active = True), i, 'IDF_active')
    results = fusion(results, ind.meanIDF(), i, 'IDF')
    results = fusion(results, ind.out_ties_per_community_members(active = True), i, 'out_ties_gini_active')
    results = fusion(results, ind.out_ties_per_community_members(), i, 'out_ties_gini')
    results = fusion(results, ind.ratio_active_members(), i, 'nb_members_active')
    results = fusion(results, ind.nb_members(), i, 'nb_members')
    
    
list_indics = list(results['1'].keys())
with open('../Results/indics_per_communtity.csv', 'w') as to_write:
    csvw = csv.writer(to_write)
    header = ['community', 'lifetime']
    for indic in list_indics:
        header.append('%s_slope' % indic)
        header.append('%s_mean' % indic)
    csvw.writerow(header)
    for com in results:
        print(results[com])
        snapshots = [int(x) for x in results[com][list_indics[0]]]
        lifetime = max(snapshots) - min(snapshots) + 1
        if lifetime <= 2:
            continue
        row = [com, lifetime]
        for indic in list_indics:
            print(indic)
            print(results[com][indic])
            u = utils(results[com][indic])
            row.append(u.slope())
            row.append(u.mean())
        csvw.writerow(row)
        
