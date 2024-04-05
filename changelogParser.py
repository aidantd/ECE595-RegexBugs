# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 21:35:29 2024

@author: Thomas
"""

import markdown
import re
import pandas as pd
#%% read in changelog file for rust engine
file = open('B:\Purdue\ECE 595 - Advanced Software Engineering\Project\ECE595-RegexBugs\CHANGELOG.md','r')

htmlmarkdown=markdown.markdown(file.read())

updates = re.findall(r"<h1>.*</h1>",htmlmarkdown) # get all headings for changes
dates = []
index = []
for update in updates:
      dates.append(re.findall(r"\(.*\)",update)) # get dates for the change
      index.append(htmlmarkdown.find(update))
      
newDates = []
years = []
for date in dates:
    if len(date) > 0:       
        newDates.append(date[0].replace(')','').replace('(',''))
        years.append(date[0][1:5])
    else:
        newDates.append(date)
        years.append(0)
    
numEvo = []
numMaintain = [] 
for iList in range(0,len(index)-1):
  # get the text between the entry headings
  entry = htmlmarkdown[index[iList]:index[iList+1]]
  bugList = re.findall('BUG',entry)
  featureList = re.findall('FEATURE',entry)
  performanceList = re.findall('PERF',entry)
  
  # count the number of updates in an entry
  numEvo.append(len(featureList) + len(performanceList))
  
  numMaintain.append(len(bugList))

entry = htmlmarkdown[index[-1]:-1]
bugList = re.findall('BUG',entry)
featureList = re.findall('FEATURE',entry)
performanceList = re.findall('PERF',entry)
  
# count the number of updates in an entry
numEvo.append(len(featureList) + len(performanceList))
  
numMaintain.append(len(bugList))

# add the parsed data to a data frame
data = {'Number Evolution': numEvo,
        'Number Maintenance': numMaintain,
        'Date': newDates,
        'Year': years}
df = pd.DataFrame(data)

# use the data frame to pull sum the values for each year 
uniqueItem = list(df['Year'].unique())
evoSumList=[]
maintainSumList= []
for item in uniqueItem:
    evoSumList.append(df['Number Evolution'][df['Year']==item].sum())
    maintainSumList.append(df['Number Maintenance'][df['Year']==item].sum())
    

sumData = {'Year': uniqueItem,
        'Number of Evolution': evoSumList,
        'Number of Maintenance': maintainSumList}
sumdf = pd.DataFrame(sumData)

sumdf.to_excel("parsedChangelog_rust.xlsx", index=False)    

# may want to normalize values for better comparison across data types 


