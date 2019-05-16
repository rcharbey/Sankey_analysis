#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:35:31 2019

@author: raphael
"""

import csv
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_samples
import math
import os
import sys

class kmeans(object):
    def __init__(self, data, nb_classes):
        self.data = pd.DataFrame.from_dict(data, orient = 'index')
        self.element_names = list(self.data.index)
        self.nb_classes = nb_classes
        self.metrics = list(self.data.columns)
        
    def to_string(self):
        print ('kmeans, k = %s, datasize = %s' % (self.nb_classes, len(self.element_names)))
    
    def get_mean_per_classe(self, element_list):
        subdata = self.data.loc[element_list]
        return subdata.describe().loc['mean']
        
    def compute(self):        
        s_max, labels_max = 0, False
        for i in range(100):
            kmeans = KMeans(n_clusters = self.nb_classes)
            kmeans.fit(self.data)
            s = np.average(silhouette_samples(self.data, kmeans.labels_))
            if s > s_max:
                labels_max = kmeans.labels_
                s_max = s
            
        self.elements_per_class = {}
        for i in range(self.nb_classes):
            self.elements_per_class[i] = []
            
        class_per_element = {}
        for i, element in enumerate(self.element_names):
            self.elements_per_class[kmeans.labels_[i]].append(element)
            class_per_element[element] = kmeans.labels_[i]
        
        self.cluster_centers = kmeans.cluster_centers_     
        return class_per_element
                    
    def write_results(self, folder):    
        
        Results = '../Results/kMeans'
        
        if not 'kMeans' in os.listdir('../Results'):
            os.mkdir(Results)
                
        with open('%s/kmeans_stats.csv' % Results, 'w') as to_write:
            csv_w = csv.writer(to_write)
            csv_w.writerow(['classe', 'effectifs']  + self.metrics)
            classe_par_taille = list(self.elements_per_class.keys())
            classe_par_taille.sort(key = lambda classe : len(self.elements_per_class[classe]))
            for classe in classe_par_taille:
                nb = len(self.elements_per_class[classe])
                mean_per_class = self.get_mean_per_classe(self.elements_per_class[classe])
                csv_w.writerow([classe, nb] + [mean_per_class[metric] for metric in self.metrics])
    
        with open('%s/typo_per_element.csv' % Results, 'w') as to_write:
            csv_w = csv.writer(to_write, delimiter =';')
            csv_w.writerow(['ego', 'class'])
            for classe in self.elements_per_class:
                for element_name in self.elements_per_class[classe]:
                    csv_w.writerow([element_name, classe])