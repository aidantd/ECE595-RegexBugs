# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 10:03:33 2024

@author: Thomas
"""
import pandas as pd
import matplotlib.pyplot as plt


def makeSingleEnginePlot(file,engine):
    # inputs:
    #   file - path to the csv with all engine data categorized, sheet names == engine names
    #   engine - string engine name wanted to make plots for 
    
#%% pull in data from csv 
    data = pd.read_excel(file,sheet_name=engine)
    data["Year"] = pd.to_datetime(data["Date"], utc=True).dt.year
    
    totalItemsPerYear = data['Year'].value_counts().sort_index()
    
    evoData = data[data['Evolution?']=='Y']
    evoItemsPerYear = evoData['Year'].value_counts().sort_index()
    
    maintainData = data[data['Evolution?']=='N']
    maintainItemsPerYear = maintainData['Year'].value_counts().sort_index()
    
    
    plt.figure()
    plt.plot(totalItemsPerYear.index, totalItemsPerYear.values, marker="o")
    plt.plot(evoItemsPerYear.index,evoItemsPerYear.values, marker="s")
    plt.plot(maintainItemsPerYear.index,maintainItemsPerYear.values, marker="^")
    plt.xlabel("Year")
    plt.ylabel("Number of Items")
    plt.title(engine.upper() + "- Number of Items Found Each Year")
    plt.legend(["All", "Evolution", "Maintenance"])
    plt.grid(True)
    #plt.show()
    plt.savefig(engine+"_line_graph_counts.png")
    


    if not (totalItemsPerYear.index == evoItemsPerYear.index).all() and not (totalItemsPerYear.index == maintainItemsPerYear.index).all():
        print('index not equal')
    else:
        plt.figure()
        plt.plot(evoItemsPerYear.index,100*evoItemsPerYear.values/totalItemsPerYear.values, marker="s")
        plt.plot(maintainItemsPerYear.index,100*maintainItemsPerYear.values/totalItemsPerYear.values, marker="^")
        plt.xlabel("Year")
        plt.ylabel("Percent of Items")
        plt.title(engine.upper() + "- Percent of Items Found Each Year")
        plt.legend(["Evolution", "Maintenance"])
        plt.grid(True)
        #plt.show()
        plt.savefig(engine+"_line_graph_percent.png")    
    

def makeAllEnginePlot(file,engines):
    # inputs:
    #   file - path to the csv with all engine data categorized, sheet names == engine names
    #   engines - list of engine names 
    
#%% pull in data from csv 
    
    # create the figures 
    evoFig = plt.figure()
    evoAxis = plt.gca()
    
    maintainFig = plt.figure()
    maintainAxis = plt.gca()
    
    # loop through the different sheets and pull in the data to plot
    for engine in engines:
        data = pd.read_excel(file,sheet_name=engine)
        data["Year"] = pd.to_datetime(data["Date"], utc=True).dt.year
        
#        totalItemsPerYear = data['Year'].value_counts().sort_index()
        
        evoData = data[data['Evolution?']=='Y']
        evoItemsPerYear = evoData['Year'].value_counts().sort_index()
        
        maintainData = data[data['Evolution?']=='N']
        maintainItemsPerYear = maintainData['Year'].value_counts().sort_index()
    
        # plot the engines over one another
        evoAxis.plot(evoItemsPerYear.index,evoItemsPerYear.values, marker="s")
        maintainAxis.plot(maintainItemsPerYear.index,maintainItemsPerYear.values, marker="s")
        
        
    # set labels and save maintenance graph    
    evoAxis.set_xlabel("Year")
    evoAxis.set_ylabel("Number of Items")
    evoAxis.set_title("Evolution Number of Items Found Each Year")
    evoAxis.legend(engines)
    evoAxis.grid(True)
    evoFig.savefig("evo_line_graph_counts.png")
    
    # set labels and save maintenance graph
    maintainAxis.set_xlabel("Year")
    maintainAxis.set_ylabel("Number of Items")
    maintainAxis.set_title("Maintenance Number of Items Found Each Year")
    maintainAxis.grid(True)
    maintainFig.savefig("maintain_line_graph_counts.png") 

########### end of function   
    
    
    
    
if __name__ == "__main__":
    file = 'B:\Purdue\ECE 595 - Advanced Software Engineering\Project\ECE595-RegexBugs\ChangeLog_pcre2_exampleOutput.xlsx'
    makeAllEnginePlot(file,["pcre2","rust"])
    makeSingleEnginePlot(file,'pcre2')
