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
        fig, ax = plt.subplots(len(bms), 1)
        for i in range(0, len(bms)):
            rects1 = ax[i].bar(x - width/2, cycles[i], width, label='GC cycles')
            rects2 = ax[i].bar(x + width/2, stalls[i], width, label='Stalls')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            #ax.set_ylabel('Scores')
            #ax.set_title('Scores by group and gender')
            ax[i].set_xticks(x, labels)
            ax[i].legend()

            ax[i].bar_label(rects1, padding=3)
            ax[i].bar_label(rects2, padding=3)
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

