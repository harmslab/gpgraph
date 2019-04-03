import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from .utils import despine, truncate_colormap

def draw_nodes(
    G,
    pos,
    ax=None,
    node_list=None,
    size=300,
    color='r',
    shape='o',
    alpha=1.0,
    linewidths=0,
    edgecolors="black",
    cmap='plasma',
    cmap_truncate=False,
    cmap_max=0.95,
    cmap_min=0.05,
    colorbar=False,
    vmin=None,
    vmax=None,
    ):
    """Draw paths in GenotypePhenotypeGraph

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

    width : float, or array of floats
       Line width of edges (default=1.0)

    cmap_truncate : bool
        Use only a subspace of the color map spectrum. If False whole color spectrum (0 to 1) is used.

    cmap_min : float (default=0.05)
        Lower bound of the color spectrum.

    cmap_max : float (default=0.95)
        Upper bound of the color spectrum.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.


    label : [None| string]
       Label for legend

    """
    # Get Figure.
    if ax is None:
        fig, ax = plt.subplots()
        despine(ax)
    else:
        fig = ax.get_figure()

    if node_list is None:
        node_list = list(G.nodes().keys())

    if vmax is None:
        phenotypes = G.gpm.phenotypes
        vmin = min(phenotypes)
        vmax = max(phenotypes)

    if cmap_truncate:
        cmap = truncate_colormap(cmap, minval=cmap_min, maxval=cmap_max)

    # Default options
    node_options = dict(
        nodelist=node_list,
        vmin=vmin,
        vmax=vmax,
        node_shape=shape,
        node_size=size,
        node_color=[G.nodes[n]['phenotypes'] for n in node_list],
        linewidths=linewidths,
        edgecolors=edgecolors,
        cmap=cmap,
        cmap_truncate=cmap_truncate,
    )

    # Draw nodes.
    nx.draw_networkx_nodes(
        G=G,
        pos=pos,
        ax=ax,
        **node_options
    )

    # Add a colorbar?
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)

        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)
