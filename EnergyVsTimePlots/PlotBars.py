import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

def prepare(bms, array1, array2, array3, labels, name_suffix, array1_label, array2_label, array3_label, norm):
    plt.rcParams["ps.useafm"] = True
    rc('font', **{'family':'sans-serif', 'sans-serif':['FreeSans']})
    plt.rcParams['pdf.fonttype'] = 42 #print(array)
    suffix = ""
    if norm != "norm":
        suffix = name_suffix
        plot(bms, array1, array2, array3, labels, suffix, array1_label, array2_label, array3_label)
    else:
        #print(array1)
        #print(array2)
        suffix = name_suffix + "_norm"
        for i in range(0, len(bms)):
            norm_gc = array1[i][0]
            norm_st = array2[i][0]
            for j in range(0, len(array1[0])):
                if norm_gc != 0:
                    array1[i][j] = array1[i][j]/norm_gc
                if norm_st != 0:
                    array2[i][j] = array2[i][j]/norm_st
        #print(array1)
        #print(array2)
        #print(array3)
        plot(bms, array1, array2, array3, labels, suffix, array1_label, array2_label, array3_label)

def plot(bms, array1, array2, array3, labels, suffix, array1_label, array2_label, array3_label):
    #print(array1)
    #print(array2)
    #print(array3)
    x = np.arange(int(len(labels)/2))  # the label locations
    width = 0.15  # the width of the bars
    if len(bms) > 1:
        fig, ax = plt.subplots(len(bms), 1,figsize= (7, len(bms)*2), sharex=True)
        for i in range(0, len(bms)):
            array1_GZ = array1[i][::2]
            array1_YinYan = array1[i][1::2]
            array2_GZ = array2[i][::2]
            array2_YinYan = array2[i][1::2]
            array3_GZ = array3[i][::2]
            array3_YinYan = array3[i][1::2]
            rects1 = ax[i].bar(x - 3*width/2, array1_GZ, width, color="black",label=array1_label + "_GZ")
            rects2 = ax[i].bar(x - width/2, array1_YinYan, width, color="grey",label=array1_label + '_YinYan')
            if "norm" not in suffix:
                ax2 = ax[i].twinx() # Create another axes that shares the same x-axis as ax.
                rects3 = ax2.bar(x + width/2, array2_GZ, width, color="salmon", label = array2_label + '_GZ')
                rects4 = ax2.bar(x + 3*width/2, array2_YinYan, width, color="pink", label = array2_label + '_YinYan')
                rects3 = ax2.bar(x + 5*width/2, array3_GZ, width, color="darkred", label = array3_label + '_GZ')
                rects4 = ax2.bar(x + 7*width/2, array3_YinYan, width, color="silver", label = array3_label + '_YinYan')
                ax2.set_ylabel(array2_label)
                lines2, labels2 = ax2.get_legend_handles_labels()
                lines, labels = ax[i].get_legend_handles_labels()
                ax[i].set_ylabel(array1_label)
                if i == 0:
                    ax[i].legend(lines + lines2, labels + labels2, loc="upper center", bbox_to_anchor=(1.7, 0.6), ncol=1, fontsize=5)
            else:
                rects3 = ax[i].bar(x + width/2, array2_GZ, width, color="salmon", label=array2_label + '_GZ')
                rects4 = ax[i].bar(x + 3*width/2, array2_YinYan, width, color="pink", label=array2_label + '_YinYan')
                rects3 = ax[i].bar(x + 5*width/2, array3_GZ, width, color="darkred", label=array3_label + '_GZ')
                rects4 = ax[i].bar(x + 7*width/2, array3_YinYan, width, color="silver", label=array3_label + '_YinYan')
                lines, labels = ax[i].get_legend_handles_labels()
                if i == 0:
                    ax[i].legend(lines, labels, loc="upper center", bbox_to_anchor=(1.7, 0.6), ncol=1, fontsize=5)
            ax[i].set_xticks(x, ["1", "1.5", "2", "2.5/4"])
            ax[i].set_title(bms[i])

        plt.setp(ax[len(bms) - 1].get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
            #ax[i].bar_label(rects2, padding=3)
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111) # Create matplotlib axes
        ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

        width = 0.15
        array1_GZ = array1[0][::2]
        array1_YinYan = array1[0][1::2]
        array2_GZ = array2[0][::2]
        array2_YinYan = array2[0][1::2]
        array3_GZ = array3[0][::2]
        array3_YinYan = array3[0][1::2]
        rects1 = ax.bar(x - 3*width/2, array1_GZ, width, color="black",label='GC_GZ')
        rects2 = ax.bar(x - width/2, array1_YinYan, width, color="grey",label='GC_YinYan')
        if "norm" not in suffix:
                rects3 = ax2.bar(x + width/2, array2_GZ, width, color="salmon", label='array2_GZ')
                rects4 = ax2.bar(x + 3*width/2, array2_YinYan, width, color="pink", label='array2_YinYan')
                ax2.set_ylabel('array2 ')
                lines2, labels2 = ax2.get_legend_handles_labels()
                lines, labels = ax.get_legend_handles_labels()
                ax.legend(lines + lines2, labels + labels2, loc=0)
        else:
                rects3 = ax.bar(x + width/2, array2_GZ, width, color="salmon", label='array2_GZ')
                rects4 = ax.bar(x + 3*width/2, array2_YinYan, width, color="pink", label='array2_YinYan')
                rects3 = ax.bar(x + 5*width/2, array3_GZ, width, color="darkred", label='array3_GZ')
                rects4 = ax.bar(x + 7*width/2, array3_YinYan, width, color="silver", label='array3_YinYan')
                lines, labels = ax.get_legend_handles_labels()
                ax.legend(lines, labels, loc=0)
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('array1')
        ax.set_xticks(x, ["1", "1.5", "2", "2.5"])
        # ask matplotlib for the plotted objects and their labels


        ax.set_title(bms[0])
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
        #ax[i].bar_label(rects2, padding=3)


    fig.tight_layout()
    #print(suffix)
    plt.savefig("./pngs/" + suffix + ".pdf", bbox_inches='tight',dpi=100)

