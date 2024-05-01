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
    plt.ylabel("Number of Commits")
    plt.title(engine.upper() + "- Number of Commits Found Each Year")
    plt.legend(["All", "Evolution", "Maintenance"])
    plt.grid(True)
    #plt.show()
    plt.savefig(engine+"_line_graph_counts.png")
    
    evoPct = []
    maintainPct = []
    for index in totalItemsPerYear.index:
        if index not in evoItemsPerYear.index:
            evoPct.append(0)
        else:
            evoPct.append(100*evoItemsPerYear[index]/totalItemsPerYear[index])
            
        if index not in maintainItemsPerYear.index:
            maintainPct.append(0)
        else:
            maintainPct.append(100*maintainItemsPerYear[index]/totalItemsPerYear[index])
                        
            
#

    plt.figure()
    plt.plot(totalItemsPerYear.index,evoPct, marker="s")
    plt.plot(totalItemsPerYear.index,maintainPct, marker="^")
    plt.xlabel("Year")
    plt.ylabel("Percent of Commits")
    plt.title(engine.upper() + "- Percent of Commits Found Each Year")
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
    
    pctEvoFig = plt.figure()
    pctEvoAxis = plt.gca()
    
    pctEvoAgeFig = plt.figure()
    pctEvoAgeAxis = plt.gca()
    
    # loop through the different sheets and pull in the data to plot
    for engine in engines:
        data = pd.read_excel(file,sheet_name=engine)
        data["Year"] = pd.to_datetime(data["Date"], utc=True).dt.year
        
        totalItemsPerYear = data['Year'].value_counts().sort_index()
        
        evoData = data[data['Evolution?']=='Y']
        evoItemsPerYear = evoData['Year'].value_counts().sort_index()
        
        maintainData = data[data['Evolution?']=='N']
        maintainItemsPerYear = maintainData['Year'].value_counts().sort_index()
        
        evoPct = []
        maintainPct = []
        for index in totalItemsPerYear.index:
            if index not in evoItemsPerYear.index:
                evoPct.append(0)
            else:
                evoPct.append(100*evoItemsPerYear[index]/totalItemsPerYear[index])
                
            if index not in maintainItemsPerYear.index:
                maintainPct.append(0)
            else:
                maintainPct.append(100*maintainItemsPerYear[index]/totalItemsPerYear[index])
                
        # plot the engines over one another
        evoAxis.plot(evoItemsPerYear.index,evoItemsPerYear.values, marker="s")
        maintainAxis.plot(maintainItemsPerYear.index,maintainItemsPerYear.values, marker="s")
        pctEvoAxis.plot(totalItemsPerYear.index,evoPct, marker="s")
        pctEvoAgeAxis.plot(totalItemsPerYear.index-totalItemsPerYear.index.tolist()[0],evoPct, marker="s")
        
    # set labels and save maintenance graph    
    evoAxis.set_xlabel("Year")
    evoAxis.set_ylabel("Number of Commits")
    evoAxis.set_title("Evolution Number of Commits Found Each Year")
    evoAxis.legend(engines)
    evoAxis.grid(True)
    evoFig.savefig("evo_line_graph_counts.png")
    
    # set labels and save maintenance graph
    maintainAxis.set_xlabel("Year")
    maintainAxis.set_ylabel("Number of Commits")
    maintainAxis.set_title("Maintenance Number of Commits Found Each Year")
    maintainAxis.legend(engines)
    maintainAxis.grid(True)
    maintainFig.savefig("maintain_line_graph_counts.png") 
    
    # set labels and save maintenance graph    
    pctEvoAxis.set_xlabel("Year")
    pctEvoAxis.set_ylabel("Percent of Commits")
    pctEvoAxis.set_title("Evolution Percent of Commits Found Each Year")
    pctEvoAxis.legend(engines)
    pctEvoAxis.grid(True)
    pctEvoFig.savefig("evo_line_graph_percent.png")
    
    # set labels and save maintenance graph    
    pctEvoAgeAxis.set_xlabel("Age [Years]")
    pctEvoAgeAxis.set_ylabel("Percent of Commits")
    pctEvoAgeAxis.set_title("Evolution Percent of Commits vs Age of Engine")
    pctEvoAgeAxis.legend(engines)
    pctEvoAgeAxis.grid(True)
    pctEvoAgeFig.savefig("evo_line_graph_percent_age.png")

########### end of function   
    
    
    
    
if __name__ == "__main__":
    file = 'B:\Purdue\ECE 595 - Advanced Software Engineering\Project\ECE595-RegexBugs\ChangeLog_pcre2_exampleOutput.xlsx'
    makeAllEnginePlot(file,["pcre2","rust"])
    makeSingleEnginePlot(file,'pcre2')
