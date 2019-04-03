import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt

def despine(ax=None):
    """Despline axes."""
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

def truncate_colormap(cmap_str, minval=0.0, maxval=1.0, n=100):
    """Truncate a colormap to a narrower subspace of the spectrum."""
    cmap = plt.get_cmap(cmap_str)
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def bins(G):
    """Bin genotypes by hamming distance from wildtype.

    Parameters
    ----------
    G : GenotypePhenotypeGraph object.
        A GenotypePhenotypeGraph object.
    """
    bins = {}
    for i in range(0, len(G.nodes("binary")[0])+1):
        bins[i] = []

    for node in range(len(list(G.nodes()))):
        node_attr = G.node[node]
        # Calculate the level of each node
        level = node_attr["binary"].count("1")
        bins[level].append(node)

    return bins
