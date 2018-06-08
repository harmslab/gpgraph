import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from .utils import despine, get_nodes_from_attributes


def draw_map_nodes(
    G,
    pos,
    ax=None,
    nodelist=None,
    vmin=None,
    vmax=None,
    cmap='plasma',
    colorbar=False,
    **kwds):
    """
    """
    # Get Figure.
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    ax = despine(ax)


    # If not node list, draw full network.
    if nodelist is None:
        nodelist = G.gpm.index

    # Get index list
    colored_nodelist = list(get_nodes_from_attributes(G, nodelist))

    # Get missing nodes list
    missing_nodelist = list(set(G.gpm.index).difference(set(colored_nodelist)))

    if vmax is None:
        phenotypes = G.gpm.phenotypes
        vmin = min(phenotypes)
        vmax = max(phenotypes)

    # Options for observed nodes
    colored_options = dict(
        pos=pos,
        nodelist=colored_nodelist,
        vmin=vmin,
        vmax=vmax,
        node_color=[G.nodes[n]['phenotypes'] for n in colored_nodelist],
        cmap=cmap,
    )
    colored_options.update(**kwds)
    nx.draw_networkx_nodes(G, **colored_options)

    # Options for missing nodes
    missing_nodelist = dict(
        pos=pos,
        nodelist=missing_nodelist,
        node_color=['white' for n in missing_nodelist],
        linewidths=1.0,
        edgecolors='k'
    )
    nx.draw_networkx_nodes(G, **missing_nodelist)

    # Add a colorbar?
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)

        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)
