#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:03:16 2019

@author: raphael
"""

from igraph import Graph
import csv

class Sgraph(object):
    
    def __init__(self):
        self.graph = Graph()
        self.vs = {}
        self.es = []
    
    @classmethod
    def from_edgelist(cls, edgelist_file):
        sgraph = cls()
        
        with open(edgelist_file) as to_read:
            csvr = csv.reader(to_read)
            next(csvr)
            
            for line in csvr:
                snapshot, id_src, id_target, com_src, com_target, link_type = line
                if not sgraph.in_graph(id_src):
                    sgraph.add_vertex(id_src, {'community' : com_src})
                if not sgraph.in_graph(id_target):
                    sgraph.add_vertex(id_target, {'community' : com_target})
                # no auto-edge
                if id_src == id_target:
                    continue
                #no double edge
                if not (id_src, id_target) in sgraph.es and not (id_target, id_src) in sgraph.es:
                    sgraph.add_edge(id_src, id_target)
        
        return sgraph
    
    def get_vertex(self, name):
        return self.vs[name]
    
    def add_vertex(self, name, kwargs = None):
        self.graph.add_vertex(name = name)
        self.vs[name] = self.graph.vs[len(self.graph.vs) - 1]
        for key in kwargs:
            self.get_vertex(name)[key] = kwargs[key]
            
    def in_graph(self, id_vertex):
        return id_vertex in self.vs
    
    def add_edge(self, id_src, id_target):
        print((self.get_vertex(id_src).index, self.get_vertex(id_target).index))
        self.graph.add_edge(self.get_vertex(id_src).index, self.get_vertex(id_target).index)
        
                
sg = Sgraph.from_edgelist('../Data/edgelists_2019-04-18_102000/edgelist_0.csv')