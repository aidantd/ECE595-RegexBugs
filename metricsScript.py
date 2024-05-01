# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:50:40 2024

@author: Thomas
"""

import createMetrics as metrics
import matplotlib.pyplot as plt
plt.close('all')
# update this file to be the master output file with each sheet as the results for a single engine
file = 'B:\Purdue\ECE 595 - Advanced Software Engineering\Project\ECE595-RegexBugs\master_outputs_OPENAI.xlsx'

# these should be the sheet names for all the engines in the output file
engines = ["re2", "icu", "pcre2"]
#["java","v8","python","pcre2","rust","re2","icu"]

# lang specific = ["java","v8","python","rust",".net","perl"]
# non lang specific = ["re2", "icu", "pcre2"]
metrics.makeAllEnginePlot(file,engines)

for engine in engines:
    metrics.makeSingleEnginePlot(file,engine)


