import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

def prepare(bms, data,  labels, name ):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    suffix = ""
    plot(bms, data, labels, name)


def plot(bms, data, labels, name):
    x = np.arange(int(len(labels)))  # the label locations
    width = 0.15  # the width of the bars
    if len(bms) > 1:
        fig, ax = plt.subplots(len(bms), 1,figsize= (7, len(bms)*2), sharex=True)
        for i in range(0, len(bms)):
            print(data[i])
            ax[i].bar(x, data[i], width, color="black")
            ax[i].set_title(bms[i])

        plt.setp(ax[len(bms) - 1].get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
            #ax[i].bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig("./pngs/" +name + ".pdf", bbox_inches='tight',dpi=100)

