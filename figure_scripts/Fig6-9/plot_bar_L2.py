import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def plot_box(data, dnames, outname, title):

    points = list()
    for i in dnames:
        tmp = data[i]
        tmp = [x for x in tmp if math.isnan(x) == False]
        points.append(tmp)

    fig, ax = plt.subplots()
    x_pos = np.arange(len(dnames))
    ax.boxplot(points, widths=0.75, whis=10)
    ax.set_ylabel('Accuracy')
    #ax.set_xticks(x_pos)
    ax.set_xticklabels(dnames)
    ax.set_title(title)
    fig.autofmt_xdate()
    ax.yaxis.grid(True)

    
    plt.savefig(outname)
    plt.show()


def plot_bar(data, dnames, outname, title, yerr = True, log = False):

    stdDeviation = list()
    average = list()

    for i in dnames:
        average.append(data[i].mean())
        stdDeviation.append(data[i].std(ddof=0))
 
    fig, ax = plt.subplots()
    x_pos = np.arange(len(dnames))
    colour = ["Red" if (x.split(" ")[0]== "MetaT") else "Blue" for x in dnames]

    if yerr:
        bars = ax.bar(x_pos, average, yerr=stdDeviation, align='center', alpha=0.5, ecolor='black', capsize=10, color = colour)
    else:
        bars = ax.bar(x_pos, average, align='center', alpha=0.5, ecolor='black', capsize=10, color = colour)
    
    if log: 
        plt.yscale("log")
        ax.set_ylabel('log L2 Norm')
    else:
        ax.set_ylabel('L2 Norm')
    

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.yaxis.grid(True)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(dnames)
    #ax.set_title(title)


    for  i in range(len(bars)):
        bar = bars[i]
        ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + bar.get_height()/100 ,
        round(average[i],4),
        horizontalalignment='center',
        color=colour[i],
        fontsize="small") 


    fig.autofmt_xdate()
   

    
    plt.savefig(outname + ".pdf")  
    plt.savefig(outname + ".svg")
    plt.show()

colormap_embedding = {

    "kmer12" : "lightblue", 
    "kmer13": "blue", 
    "Hash" : "green",
    "LSH15_b23" : "yellow", 
    "ML" : "red" ,
    "DeepM" : "grey" 
}

colormap_all = {
    "DeepM" : "grey",
    "Kaiju" : "brown",
    "Kraken" : "lightgreen",
    "Kraken 2" : "green",
    "Centrifuge" : "yellow",
    "Diamond-MEGAN" : "pink",
    "BLAST-MEGAN" : "purple",
    "CLARK" : "lightred",
    "CLARK-S" : "red",
    "MetaT k12" : "lightblue",
    "MetaT k13": "blue"
}





data = pd.read_csv("result_mock_species.csv")
data1 = pd.read_csv("result_mock_genus.csv")
data2 = pd.read_csv("metaT_vs_all_mock_genus.csv")
data3 = pd.read_csv("result_unknown_all.csv")
data4 = pd.read_csv("bench_res_all.csv")

outname = "mock_species"
outname1 = "embedding_mock_genus"
outname2 = "metaT_vs_all_mock_genus"
outname3 = "result_unknown_all"
outname4 = "bench_res_"

title0 = 'L2 Norm of abundance error for MOCK genus of different embeddings'
title1 = 'L2 Norm of abundance error for MOCK genus'
title2 = 'L2 Norm of abundance error for MOCK species'
title3 = 'L2 Norm of abundance error for absent species'
title4 = 'Accuracy of deepM and MetaT on benchmark genus datasets'
title5 = 'Accuracy of deepM and MetaT on benchmark species datasets'

print(data4)
dnames = data.columns.to_list()[1:]
dnames1 = data1.columns.to_list()[1:]
dnames2 = data2.columns.to_list()[1:]
dnames3 = data3.columns.to_list()[1:]
dnames4 = data4.columns.to_list()

plot_bar(data, dnames, outname, title2)
plot_bar(data1, dnames1, outname1, title0)
plot_bar(data2, dnames2, outname2, title1)
plot_bar(data3, dnames3, outname3, title3, False, True)
#plot_hist(data4, dnames4, outname4, title4)
plot_box(data4[dnames4[0:3]], dnames4[0:3], outname4 + "genus", title4)
plot_box(data4[dnames4[3:6]], dnames4[3:6], outname4 + "species", title5)

