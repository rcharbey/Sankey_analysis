#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:28:19 2019

@author: raphael
"""

from PMGraph import PMGraph
    
pmg = PMGraph.read('../Data/edgescommunities')
for i in pmg.temporal_communities:
    tc = pmg.temporal_communities[i]
    tc.plot_evolution()