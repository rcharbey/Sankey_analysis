# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import csv

class PMVertex(object):
    def __init__(self, pmgraph, id_vertex, community, snapshot, nb_members):
        self.pmgraph = pmgraph
        self.id = id_vertex
        self.community = community
        self.snapshot = snapshot
        self.nb_members = nb_members
        
    def get_mask_vector(self):
        
        in_vector = []
        if not self.snapshot == 0:
            for pme_in in self.pmgraph.edge_set_sequence[self.snapshot - 1]:
                if pme_in.target == self.id:
                    in_vector.append(pme_in.weight)
                    
        
        out_vector = []
        if not self.snapshot == len(self.pmgraph.vertex_set_sequence) - 1:
            for pme_out in self.pmgraph.edge_set_sequence[self.snapshot]:
                if pme_out.source == self.id:
                    out_vector.append(pme_out.weight)
                    
        return (in_vector, out_vector)

        
class PMEdge(object):
    def __init__(self, pmgraph, snapshot, pmvertex_1_id, pmvertex_2_id, weight):
        self.pmgraph = pmgraph
        self.source = pmvertex_1_id
        self.target = pmvertex_2_id
        self.snapshot_from = snapshot
        self.snapshot_to = snapshot + 1
        self.weight = weight
        

class PMGraph(object):
    def __init__(self, vertex_set_sequence, edge_set_sequence):
        self.all_vertices = []
        self.all_edges = []
        self.vertex_set_sequence = [{} for x in range(len(vertex_set_sequence))] 
        self.edge_set_sequence = [[] for x in range(len(edge_set_sequence))]
        
        nb_vertices = 0
        
        for i in range(len(vertex_set_sequence)):
            for v, nb in vertex_set_sequence[i]:
                pmvertex = PMVertex(self, nb_vertices, v, i, nb)
                self.all_vertices.append(pmvertex)
                self.vertex_set_sequence[i][v] = pmvertex
                nb_vertices += 1
                
        for i in range(len(edge_set_sequence)):
            for vertex_1, vertex_2, w in edge_set_sequence[i]:
                pmv_1_id = self.vertex_set_sequence[i][vertex_1]
                pmv_2_id = self.vertex_set_sequence[i+1][vertex_2]
                pmedge = PMEdge(self, i, pmv_1_id, pmv_2_id, w)
                self.all_edges.append(pmedge)
                self.edge_set_sequence[i].append(pmedge)
        
    @classmethod
    def read(cls, filename):
        _max_snapshot = -1
        _vertex_set_sequence = []
        with open(filename + '_nb_members_per_community.csv', 'r') as to_read:
            csvr = csv.reader(to_read)
            next(csvr)
            for line in csvr:
                snapshot, community_1, nb_members = (int(x) for x in line)
                if snapshot > _max_snapshot:
                    _vertex_set_sequence.append(set())
                    _max_snapshot = snapshot
                _vertex_set_sequence[snapshot].add((community_1, nb_members))
         
        _edge_set_sequence = [[] for x in range(_max_snapshot)]          
        with open(filename + '_flows.csv', 'r') as to_read:
            csvr = csv.reader(to_read)
            next(csvr)
            for line in csvr:
                snapshot, community_1, community_2, weight = (int(x) for x in line)
                _edge_set_sequence[snapshot].append((community_1, community_2, weight))
           
        return cls(_vertex_set_sequence, _edge_set_sequence)
    
    def get_mask_vectors(self):
        return {pmv.id : pmv.get_mask_vector() for pmv in self.all_vertices}
    
    def get_nb_members(self):
        return {pmv.id : pmv.nb_members for pmv in self.all_vertices}
            
    def get_snapshots(self):
        return {pmv.id : pmv.snapshots for pmv in self.all_vertices}
    
    def get_community(self):
        return {pmv.id : pmv.community for pmv in self.all_vertices}
    
PMGraph.read('../Data/edgescommunities').get_mask_vectors()
        
            
            