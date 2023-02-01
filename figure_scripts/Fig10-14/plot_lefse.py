import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch
import os



def read_files(abun_path, points_path, s_data_path):
  
    abun = pd.read_csv(abun_path,header = None)
        
    points = pd.read_csv(points_path, sep="\t", header = None)
    points = points[points[2].notnull().tolist()]
    
    index = ["Taxon", "Host_disease"]
    index.extend(points[0].tolist())
    metadata = points.iloc[:,[0,2]]

    data = abun[[x in index for x in abun[0]]]
    data = data.transpose()
    data.columns = data.iloc[0,:].tolist()
    data = data.iloc[1:,:]
    print(data)
    metadata = metadata.sort_values(by=[0])
    print(metadata)

    species = pd.read_csv(s_data_path)
    species = species.iloc[[x in metadata[0].tolist() for x in species["Genome"]],:]
    print(species)
    genus = [species.loc[ species.index.tolist()[x], species["Assignment_level"].tolist()[x]] for x in range(len(species["Assignment_level"].tolist()))]
    genus = pd.DataFrame({"Genus":genus, "Genome":species["Genome"]})
    genus["Disease"] = metadata[2].tolist()
    print (genus)

    points.columns = ["Species", "Median Abundance", "group","LDA", "p-value"]

    return data, genus, points


def plot_data(data, metadata, out_path):

    try:
        os.mkdir(out_path)
    except:
        pass

    data = data.sort_values(by="Host_disease")
    print(data)
    head = data.iloc[:,0:2]
    data = data.iloc[:,2:]
    disease = head["Host_disease"].unique().tolist()
    diseases = metadata["Disease"].tolist()
    species = metadata["Genome"].tolist()
    genus = metadata["Genus"].tolist()


    for j in range(len(diseases)):   
        
        #print(species)
        #print(data[species])
        tmp = data[species[j]].astype(float) 
        #tmp *= 1000000

        colors = ["blue","red","green","orange"]
        fig, ax = plt.subplots()
        for i in range(len(disease)):
            t = tmp[[x == disease[i] for x in head["Host_disease"]]] 
            sns.distplot(t, hist = False, kde=True, color = colors[i], hist_kws={'edgecolor':'black'}, kde_kws={'shade': True,'linewidth': 2}, label=disease[i])
        #plt.plot([0,0], [0,2000], 'k-', lw=2)
        ax.legend(prop={'size': 14}, title = 'Disease', loc = 7)
        ax.set_title(species[j] + " (" + genus[j] + ") " + diseases[j])
        #ax.set_title('Density of Normalized Abundance from ' + species)
        ax.set_xlabel('Normalized Abundance')
        ax.set_ylabel('Density')
        plt.yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.yaxis.grid(True)
        plt.savefig(out_path + "/" + "plot_lefse_" + species[j] + ".pdf" )
        plt.close()

def plot_deep(data, metadata, out_path):
    #DeepMicrobes style plot

    data = data.sort_values(by="Host_disease")
    print(data)
    head = data.iloc[:,0:2]
    data = data.iloc[:,2:].astype(float)
    disease = head["Host_disease"].unique().tolist()
    diseases = metadata["Disease"].tolist()
    species = metadata["Genome"].tolist()
    genus = metadata["Genus"].tolist()

    data_normed = data.copy()

    j=1

    data_healthy = data[head["Host_disease"] == "control"]

    means = data_healthy.describe().iloc[1,:]
    medians  = data_healthy.median(axis=0)

    for i in medians.index.tolist():
        data_normed[i] /= medians[i]

    

    tmp = data[species]#.astype(float) 
    #tmp *= 1000000
   
    colors = ["blue","red","green","orange"]

    #plt.hist(tmp , color = "blue", edgecolor = "black", bins = 10)
    fig, ax = plt.subplots()
    for i in range(len(disease)):
        t = tmp[[x == disease[i] for x in head["Host_disease"]]] 
        sns.distplot(t, hist = False, kde=True, color = colors[i], hist_kws={'edgecolor':'black'}, kde_kws={'shade': True,'linewidth': 2}, label=disease[i])
    #plt.plot([0,0], [0,2000], 'k-', lw=2)
    ax.legend(prop={'size': 14}, title = 'Disease', loc = 7)
    #ax.set_title('Density of Normalized Abundance from ' + species)
    ax.set_title(species[j] + " (" + genus[j] + ") " + diseases[j])
    ax.set_xlabel('Normalized Abundance')
    ax.set_ylabel('Density')
    plt.yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.yaxis.grid(True)
    plt.show()

def plot_bar(points, metadata):
    
    #fig, ax = plt.subplots()
    metadata = metadata.sort_values(by="Genome")
    points = points.sort_values(by="Species")
    metadata = metadata.reset_index()
    points = points.reset_index()
    print(points)
    print(metadata)

    colors = ["blue","red","green","orange"]

    label = metadata["Genome"] + "(" + metadata["Genus"] + ")"
    
    print(label)

    points["label"] = label
    print(points)

    points = points.sort_values(by="group")
    group = points["group"].tolist()

    colours = list()
    for i in group:
        if (i == "cd"):
            colours.append("blue")
        if (i == "control"):
            colours.append("red")
        if (i == "uc"):
            colours.append("green")

    cs = {"cd":"blue", "control":"red", "uc":"green"} 
    #ax = points.plot.barh(x="Species", y="LDA", color=colours)
    ax = points.plot.barh(x="label", y="LDA", color=points["group"].replace(cs), alpha= 0.7)
    ax.legend(
        [
            Patch(facecolor = cs["uc"]),
            Patch(facecolor = cs["control"]),
            Patch(facecolor = cs["cd"])
        ], ["uc", "control", "cd"]
    ) 


    max = round(points["LDA"].max())
    print (max)
    for i in np.arange(0, max + 0.5, 0.5):
        plt.axvline(x=i, color = "black", linestyle = "--", linewidth = 0.5)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.yaxis.grid(False)
    ax.set_xlabel('LDA score (log₍₁₀₎)')
    ax.set_ylabel('Species')    
    #ax.set_title('LDA score of significant species')

    plt.tight_layout()
    plt.savefig("plot_LDA_.pdf" )
    plt.show()
    plt.close()

    return 0

def main ():

    parser = argparse.ArgumentParser(description="Plot lefse data")
    parser.add_argument("--a", dest="abundances", type=str, required=True)
    parser.add_argument("--d", dest="datapoints", type=str, required=True)
    parser.add_argument("--s", dest="species_metadata", type=str, required=True)
    parser.add_argument("--o",dest="outfile", type=str, required=True)
    args = parser.parse_args()  


    abun_path = args.abundances
    points_path = args.datapoints
    out_path = args.outfile
    s_data_path = args.species_metadata

    data, metadata, points  = read_files(abun_path, points_path, s_data_path)


    #plot_data(data,metadata, out_path)
    #plot_deep(data,metadata, out_path)
    plot_bar(points, metadata)
    

if __name__ == "__main__":
    main()