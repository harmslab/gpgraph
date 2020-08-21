import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from .utils import despine

docs = """
Draw paths in GenotypePhenotypeGraph

    Parameters
    ----------
    G : graph
       A networkx graph
    
    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    edgelist : collection of edge tuples
       Draw only specified edges(default=G.edges())

    edge_widths : float, or array of floats
       Relative Line width of edges (default=1.0). Use scalar to chat width.

    edge_scalar : float
       Scale all edges (default=1.0)

    edge_color : color string, or array of floats
       Edge color. Can be a single color format string (default='r'),
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    style : string
       Edge line style (default='solid') (solid|dashed|dotted,dashdot)

    alpha : float
       The edge transparency (default=1.0)

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


def draw_edges(
        G,
        pos,
        ax=None,
        edge_list=None,
        widths=1.0,
        scalar=1.0,
        colors="black",
        style="solid",
        alpha=1.0,
        arrows=False,
        arrowstyles="-|>",
        arrowsize=10
):
    # Get Figure.
    if ax is None:
        fig, ax = plt.subplots()
        despine(ax)
    else:
        fig = ax.get_figure()

    if widths is None:
        width = scalar
    else:
        width = scalar * np.array(widths)

    edge_options = dict(
        edgelist=edge_list,
        width=widths,
        scalar=scalar,
        edge_color=colors,
        style=style,
        alpha=alpha,
        arrows=arrows,
        arrowstyles=arrowstyles,
        arrowsize=arrowsize
    )

    # Draw edges
    nx.draw_networkx_edges(G=G, pos=pos, ax=ax, **edge_options)
