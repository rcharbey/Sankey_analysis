#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:03:16 2019

@author: raphael
"""

from igraph import Graph
import csv
import itertools
from Graphs.graph_utils import Admin


class Sedge(object):
    def __init__(self, svertex_1, svertex_2):
        self.sv1 = svertex_1
        self.sv2 = svertex_2
        self.active = False
        self.common_threads = svertex_1.all_threads & svertex_2.all_threads
        self.common_active_threads = svertex_1.active_threads & svertex_2.active_threads
        
    def activate(self):
        self.active = True
        
    def is_active(self):
        return self.active

class Svertex(object):
    def __init__(self, sgraph, name, community, active_threads, all_threads, vertex):
        self.sgraph = sgraph
        self.vertex = vertex
        self.name = name
        self.community = community
        self.active_threads = set(active_threads)
        self.all_threads = set(all_threads)
        self.nb_messages = len(active_threads)
        self.is_active = len(self.active_threads) != 0
        self.id = vertex.index
        self.neighbors = {}
        self.adjacent_edges = {}
        self.community.add_member(self)
        
    def degree(self, active = False):
        return len(self.get_adjacent_edges(active))
        
    def is_active_in_thread(self, thread):
        return thread in self.active_threads
    
    def number_co_active_threads(self, svertex):
        return len(self.svertex.active_threads & svertex.active_threads)
    
    #Check that the intersection of the active threads of the two svertices is not empty
    def is_co_active(self, svertex):
        return self.number_co_active_threads(svertex) != 0
    
    def neighbors(self):
        return self.neighbors.values()
    
    def is_neighbor(self, svertex):
        return svertex.id in self.neighbors.keys()
    
    def add_neighbor(self, svertex):
        self.neighbors[svertex.id] = svertex
        
    def get_adjacent_edges(self, active = False):
        if active:
            return [se for se in self.adjacent_edges.values() if se.is_active()]
        return self.adjacent_edges.values()

    def add_adjacent_edge(self, sedge, neighbor):
        self.adjacent_edges[neighbor] = sedge
     
class Scommunity(object):
    def __init__(self, sgraph, index):
        self.sgraph = sgraph
        self.id = index
        self.members = set()
        self.nb_active_members = 0
        self.nb_members = 0
        self.sgraph.communities[index] = self
        
    def add_member(self, snapshot_vertex):
        self.members.add(snapshot_vertex)
        self.nb_members += 1
        if snapshot_vertex.is_active:
            self.nb_active_members += 1
        
    def get_active_members(self):
        return [svertex for svertex in self.members if svertex.is_active]   
        
class Sgraph(object):
    
    def __init__(self, snapshot):
        self.graph = Graph()
        self.vs = []
        self.es = []
        self.snapshot = snapshot
        self.active_threads = set()
        self.vertex_by_name = {}
        self.communities = {}
        
    def to_print(self):
        print('number of vertices : %s - (active : %s)' % (len(self.vs), len(self.get_active_vertices())))
        print('number of edges : %s - (active : %s)' % (len(self.es), len(self.get_active_edges())))
        
    def write(self):
        Admin.write_graph(self.graph, '../Graphs/%s.gml' % self.snapshot)        
    
    @classmethod
    def from_base(cls, base_file, this_snapshot):
        sgraph = cls(this_snapshot)
        sgraph.bug = 0
        
        sgraph.authors_per_thread = {}
        sgraph.threads_per_author = {}
        sgraph.active_threads_per_author = {}
        sgraph.community_per_vertex = {}
        
        active_threads = set()
        
        vertices_to_add = []
        with open(base_file, 'r') as to_read:
            csvr = csv.reader(to_read)
            next(csvr)
            for line in csvr:
                
                author, id_author, snapshot, community_id = line[0:4]
                snapshot = int(snapshot)
                threads = line[4:]
                
                if snapshot == sgraph.snapshot:
                    active_threads.update(threads)
                    sgraph.active_threads_per_author[author] = threads
                    
                    if not community_id in sgraph.communities:
                        Scommunity(sgraph, community_id)
                    community = sgraph.communities[community_id]
                    
                    vertices_to_add.append((author, community, threads))
                
                                           
                    
                if snapshot <= sgraph.snapshot:
                    if not author in sgraph.threads_per_author:
                        sgraph.threads_per_author[author] = set()
                    for thread in threads:
                        if not thread in sgraph.authors_per_thread:
                            sgraph.authors_per_thread[thread] = set()
                        sgraph.authors_per_thread[thread].add(author)
                        sgraph.threads_per_author[author].add(thread)
                        
            for author, community, threads in vertices_to_add:
                sgraph.add_vertex(author, community, threads, sgraph.threads_per_author[author])
            
            for thread in active_threads:
                for author_1, author_2 in itertools.combinations(sgraph.authors_per_thread[thread], 2):
                    sv1 = sgraph.get_vertex_by_name(author_1)
                    sv2 = sgraph.get_vertex_by_name(author_2)
                    se = sgraph.add_edge(sv1, sv2)
                    if sv1.is_active_in_thread(thread) and sv2.is_active_in_thread(thread):  
                        se.activate()
        return sgraph
    
    def get_vertex_by_name(self, name):
        return self.vertex_by_name[name]

    def get_vertex_by_graph_id(self, gid):
        return self.graph.vs[gid]
    
    def add_vertex(self, author, community, active_threads, all_threads):
        self.graph.add_vertex({'community' : community.id, 'author' : author, 'threads' : active_threads})
        sv = Svertex(self, author, community, active_threads, all_threads, self.graph.vs[len(self.graph.vs) - 1])
        self.vs.append(sv)
        self.vertex_by_name[author] = sv
            
    def in_graph(self, vertex_name):
        return vertex_name in self.vs
    
    def add_edge(self, sv1, sv2):
        
        self.graph.add_edge(sv1.id, sv2.id)
        se = Sedge(sv1, sv2)
        sv1.add_adjacent_edge(se, sv2.id)
        sv2.add_adjacent_edge(se, sv1.id)
        self.es.append(se)
        sv1.add_neighbor(sv2)
        sv2.add_neighbor(sv1)
        return se
    
    def get_edge(self, sv1, sv2):
        return sv1.get_adjacent_edges()[sv1.id]
            
    def get_active_vertices(self):
        return [x for x in self.vs if x.active_threads]
    
    def get_active_edges(self):
        return [se for se in self.es if se.is_active]
    
    def get_communities(self):
        return self.communities.values()
    
sg = Sgraph.from_base('../Data/Active_network_base/build_active_network_base.csv', 5)
