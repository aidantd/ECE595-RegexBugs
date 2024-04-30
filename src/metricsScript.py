# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:50:40 2024

@author: Thomas
"""

import createMetrics as metrics

# update this file to be the master output file with each sheet as the results for a single engine
file = 'B:\Purdue\ECE 595 - Advanced Software Engineering\Project\ECE595-RegexBugs\ChangeLog_pcre2_exampleOutput.xlsx'

# these should be the sheet names for all the engines in the output file
engines = ["pcre2","rust"]
metrics.makeAllEnginePlot(file,engines)

for engine in engines:
    metrics.makeSingleEnginePlot(file,engine)


