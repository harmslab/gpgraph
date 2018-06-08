import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from .utils import despine
from ..paths import paths_prob_to_edges_flux

def draw_paths(
    G,
    pos,
    paths,
    ax=None,
    edge_equal=False,
    edge_scalar=1.0,
    edge_color='k',
    style='solid',
    edge_alpha=1.0,
    arrows=False,
    arrowstyle='-|>',
    arrowsize=10,
    ):
    """Draw paths in GenotypePhenotypeGraph

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

    edgelist : collection of edge tuples
       Draw only specified edges(default=G.edges())

    width : float, or array of floats
       Line width of edges (default=1.0)

    edge_color : color string, or array of floats
       Edge color. Can be a single color format string (default='r'),
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    style : string
       Edge line style (default='solid') (solid|dashed|dotted,dashdot)

    alpha : float
       The edge transparency (default=1.0)

    edge_ cmap : Matplotlib colormap
       Colormap for mapping intensities of edges (default=None)

    edge_vmin,edge_vmax : floats
       Minimum and maximum for edge colormap scaling (default=None)

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    arrows : bool, optional (default=True)
       For directed graphs, if True draw arrowheads.
       Note: Arrows will be the same color as edges.

    arrowstyle : str, optional (default='-|>')
       For directed graphs, choose the style of the arrow heads.
       See :py:class: `matplotlib.patches.ArrowStyle` for more
       options.

    arrowsize : int, optional (default=10)
       For directed graphs, choose the size of the arrow head head's length and
       width. See :py:class: `matplotlib.patches.FancyArrowPatch` for attribute
       `mutation_scale` for more info.

    label : [None| string]
       Label for legend

    """
    # Get Figure.
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    ax = despine(ax)

    # Get flux through edges
    edges = paths_prob_to_edges_flux(paths)
    edgelist = list(edges.keys())

    edge_widths = np.array(list(edges.values()))
    if edge_equal:
        # Remove for zero prob edges
        edge_widths[edge_widths > 0] = 1
        width = edge_scalar * edge_widths
    else:
        width = edge_scalar * edge_widths

    # Draw edges
    nx.draw_networkx_edges(
        G=G,
        pos=pos,
        edgelist=edgelist,
        width=width,
        edge_color=edge_color,
        ax=ax,
        style=style,
        alpha=edge_alpha,
        arrows=arrows,
        arrowstyle=arrowstyle,
        arrowsize=arrowsize,
    )
