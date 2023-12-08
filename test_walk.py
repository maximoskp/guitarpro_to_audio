#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 22:34:19 2023

@author: max
"""

import os

path_to_dataset = '/Volumes/maXpand/datasets/DadaGP-v1.1'

for root, subdirs, files in os.walk( path_to_dataset ):
    print('root: ', root.replace(path_to_dataset, ''))
    print('subdirs: ', subdirs)
    print('files: ', files)