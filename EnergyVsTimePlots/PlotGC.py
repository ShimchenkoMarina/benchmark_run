import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

def plot(bms, cycles, stalls, labels):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    if len(bms) > 1:
        fig, ax = plt.subplots(len(bms), 1, sharex=True)
        for i in range(0, len(bms)):
            ax2 = ax[i].twinx() # Create another axes that shares the same x-axis as ax.
            rects1 = ax[i].bar(x - width/2, cycles[i], width, color="black",label='GC cycles')
            rects2 = ax2.bar(x + width/2, stalls[i], width, color="grey", label='Stalls')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax[i].set_ylabel('Cycles')
            ax2.set_ylabel('Stalls ')
            #ax[i].set_xticks(x, labels)
            # ask matplotlib for the plotted objects and their labels
            lines, labels = ax[i].get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax[i].legend(lines + lines2, labels + labels2, loc=0)


            ax[i].set_title(bms[i])
        plt.setp(ax[len(bms) - 1].get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
            #ax[i].bar_label(rects2, padding=3)
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111) # Create matplotlib axes
        ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

        width = 0.4

        ax.bar(x - width/2, cycles[0], width, color= "black", label="GC cycles")
        ax2.bar(x + width/2, stalls[0], width, color = "grey", label="Stalls")

        ax.set_ylabel('Cycles')
        ax2.set_ylabel('Normalized stalls ')

        ax.set_xticks(x, labels)
        ax.legend()

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    fig.tight_layout()
    plt.savefig("./pngs/StallsGC.pdf", bbox_inches='tight',dpi=100)

