import numpy as np
import sys
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering


def plot_dendrogram(num_cl, model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count
    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)
    # Plot the corresponding dendrogram
    fl = fcluster(linkage_matrix,num_cl, criterion='maxclust')
    with open("bridge_for_clustering.txt", 'w') as writer:
        writer.write(str(fl))
    dendrogram(linkage_matrix, **kwargs)
    

def setup_dendrogram(data, bms, name):
    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(distance_threshold=None, n_clusters=len(data), compute_distances=True)
    model = model.fit(data)
    plt.title("Hierarchical Clustering Dendrogram")
    # plot the top three levels of the dendrogram
    plot_dendrogram(len(bms), model, truncate_mode="level", orientation="right", labels=list(bms), leaf_font_size=4)
    plt.savefig(name, bbox_inches='tight', dpi=200)
    plt.close()


if __name__ == '__main__':
    data = sys.arg[1]
    bms = sys.arg[2]
    name = sys.arg[3]
    fl = setup_dendrogram(data, bms,name)
