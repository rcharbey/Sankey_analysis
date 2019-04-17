#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:54:09 2019

@author: raphael
"""

from matplotlib.pyplot import savefig, close, plot, legend, xticks
from numpy import arange


class Temporal_community(object):
    def __init__(self, pmgraph, community_id, pmvertices = None):
        self.pmgraph = pmgraph
        self.id = community_id
        if pmvertices is None:
            self.members = []
            self.lifetime = None
        else:
            self.members = pmvertices
            list_snapshots = [member.snapshot for member in self.members]
            self.lifetime = (min(list_snapshots), max(list_snapshots))
        self.members.sort(key=lambda x : x.snapshot)
        
    def add(self, pmvertex):
        self.members.append(pmvertex)
        self.members.sort(key=lambda x : x.snapshot)
        this_snapshot = pmvertex.snapshot
        if self.lifetime is None:
            self.lifetime = (this_snapshot, this_snapshot)
        if this_snapshot < self.lifetime[0]:
            self.lifetime = (this_snapshot, self.lifetime[1])
        if this_snapshot > self.lifetime[1]:
            self.lifetime = (self.lifetime[0], this_snapshot)
        
    def plot_evolution(self):
        print(self.id)
        d_in, d_out, nb_members = [], [], []
        for pmv in self.members:
            vector_in, vector_out = pmv.get_mask_vector()
            d_in.append(len(vector_in))
            d_out.append(len(vector_out))
            nb_members.append(pmv.nb_members)
          
        print('lifetime %s %s' % self.lifetime)
        print('d_in %s' % (d_in))
        print('d_out %s' % d_out)
        print('members %s' % nb_members)
        
        plot(d_in, label = 'd_in')
        plot(d_out, label = 'd_out')
        plot(nb_members, label = 'members')
        xticks(range(len(d_in)), arange(self.lifetime[0], self.lifetime[1] + 1, step = 1))
        legend(loc = 'upper right')
        savefig('../Results/Plot_per_community/%s.png' % self.id)
        close()
        
            
            
