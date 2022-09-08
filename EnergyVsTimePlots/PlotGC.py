import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

def prepare(bms, cycles, stalls, maxpause, labels, name_suffix):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    suffix = name_suffix
    #print(len(cycles))
    plot(bms, cycles, stalls, maxpause, labels, suffix)
    suffix = suffix + "_norm"
    #print(len(bms))
    for i in range(0, len(bms)):
        norm_gc = cycles[i][0]
        norm_st = stalls[i][0]
        for j in range(0, len(cycles[0])):
            #print(i)
            #print(j)
            if norm_gc != 0:
                cycles[i][j] = cycles[i][j]/norm_gc
            if norm_st != 0:
                stalls[i][j] = stalls[i][j]/norm_st
    #print(len(cycles))
    plot(bms, cycles, stalls, maxpause, labels, suffix)

def plot(bms, cycles, stalls, maxpause, labels, suffix):
    x = np.arange(int(len(labels)/2))  # the label locations
    width = 0.15  # the width of the bars
    if len(bms) > 1:
        fig, ax = plt.subplots(len(bms), 1,figsize= (5, len(bms)*2), sharex=True)
        for i in range(0, len(bms)):
            cycles_GZ = cycles[i][::2]
            cycles_YinYan = cycles[i][1::2]
            stalls_GZ = stalls[i][::2]
            stalls_YinYan = stalls[i][1::2]
            maxpause_GZ = maxpause[i][::2]
            maxpause_YinYan = maxpause[i][1::2]
            #print(cycles_GZ)
            #print(cycles_YinYan)
            rects1 = ax[i].bar(x - 3*width/2, cycles_GZ, width, color="black",label='GC_GZ')
            rects2 = ax[i].bar(x - width/2, cycles_YinYan, width, color="grey",label='GC_YinYan')
            if "norm" not in suffix:
                ax2 = ax[i].twinx() # Create another axes that shares the same x-axis as ax.
                rects3 = ax2.bar(x + width/2, stalls_GZ, width, color="salmon", label='Stalls_GZ')
                rects4 = ax2.bar(x + 3*width/2, stalls_YinYan, width, color="pink", label='Stalls_YinYan')
                ax2.set_ylabel('Stalls ')
                lines2, labels2 = ax2.get_legend_handles_labels()
                lines, labels = ax[i].get_legend_handles_labels()
                if i == 0:
                    ax[i].legend(lines + lines2, labels + labels2, loc=0)
            else:
                rects3 = ax[i].bar(x + width/2, stalls_GZ, width, color="salmon", label='Stalls_GZ')
                rects4 = ax[i].bar(x + 3*width/2, stalls_YinYan, width, color="pink", label='Stalls_YinYan')
                rects3 = ax[i].bar(x + 5*width/2, maxpause_GZ, width, color="darkred", label='MaxPause_GZ')
                rects4 = ax[i].bar(x + 7*width/2, maxpause_YinYan, width, color="silver", label='MaxPause_YinYan')
                lines, labels = ax[i].get_legend_handles_labels()
                if i == 0:
                    ax[i].legend(lines, labels, loc=0)
            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax[i].set_ylabel('Cycles')
            ax[i].set_xticks(x, ["1", "1.5", "2", "2.5/4"])
            # ask matplotlib for the plotted objects and their labels


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
    plt.savefig("./pngs/StallsGC" + suffix + ".pdf", bbox_inches='tight',dpi=100)

