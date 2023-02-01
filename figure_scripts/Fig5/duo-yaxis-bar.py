import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


colormap_all = ["red", "blue", "green"]



data = pd.read_csv('kmer_prec_rec_loss.txt')
print(data)

df = data.iloc[:,4:7]
df.columns = ['precision','recall','loss']
df.index = data["k"]

_ = df.plot( kind= 'bar' , secondary_y= 'loss' , rot= 0, color=colormap_all , alpha= 0.7, capsize=10 )
#_ = df.plot( kind= 'bar' , secondary_y= 'loss' , rot= 0 )

ax1, ax2 = plt.gcf().get_axes() 

ax1.set_ylabel('Precision / Recall')
ax2.set_ylabel('Loss')


ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#DDDDDD')
ax1.yaxis.grid(True)
ax1.set_yticks(np.arange(0, 1.2, step=0.2))
ax1.set_ylim(0,1)


ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_color('#DDDDDD')
ax2.set_yticks(np.arange(0, 3, step=0.5))
ax2.set_ylim(0,2.5)

# Put a legend below current axis
handles, labels = [(a + b) for a, b in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
labels = ["Precision", "Recall", "Loss"]
ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.1),
          fancybox=True, shadow=True, ncol=5, frameon=False)

ax1.set_xlabel("kmer size")

plt.savefig("kmer_prec_recall_loss.pdf" + ".pdf")  
plt.show()