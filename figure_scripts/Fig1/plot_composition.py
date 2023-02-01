import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_bar(points):
    
    _ = points.plot( kind= 'barh' , rot= 0, color="Blue" , alpha= 0.5, legend = False )
    
    ax = plt.gca() 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.yaxis.grid(False)
    ax.set_xlabel('Count')
    ax.set_ylabel('Genus')

    ax.set_xticks(np.arange(0, 1100, step=100))
    ax.xaxis.grid(True)



    plt.tight_layout()
    plt.savefig("hgr_composition.pdf" )
    plt.show()
    plt.close()

    return 0



data = pd.read_csv("hgr_composition.csv")
data = data.iloc[:,0:9]
data = data.iloc[:,[0,8]]
print(data)
data = data.iloc[:,1:2]

stat = data.groupby("Genus").value_counts()
stat = stat.sort_values(ascending=False)

top = stat[0:11]


top_names = top.index.tolist()
top_val = top.values

rest = stat.drop(top_names)
classified = top.sum() + rest.sum()
unclassified = 2505 - classified

top = top.append(pd.Series([rest.sum(),unclassified], index = ["Rest", "Unclassified"] ))
top = top.sort_values(ascending=False)
top = top.to_frame()
print (top)

plot_bar(top)



