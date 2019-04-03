import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from .nodes import draw_nodes
from .edges import draw_edges
from .utils import despine
from .pos import flattened


def draw_gpgraph(
    G,
    pos=None,
    ax=None,
    figsize=None,
    edge_list=None,
    edge_widths=1.0,
    edge_scalar=1.0,
    edge_colors="black",
    edge_style="solid",
    edge_alpha=1.0,
    edge_arrows=False,
    edge_arrowstyles="-|>",
    edge_arrowsize=10,
    node_list=None, 
    node_size=300,
    node_color="r",
    node_shape="o",
    node_alpha=1.0,
    node_linewidths=0,
    node_edgecolors="black",
    cmap="plasma",
    cmap_truncate=False,
    cmap_max=0.95,
    cmap_min=0.05,
    colorbar=False,
    vmin=None,
    vmax=None
    ):
    """Draw the GenotypePhenotypeGraph using Matplotlib.

    Draw the graph with Matplotlib with options for node positions,
    labeling, titles, and many other drawing features.
    See draw() for simple drawing without labels or axes.

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See :py:mod:`networkx.drawing.layout` for functions that
       compute node positions.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    edge_list : list, optional (default=G.edges())
       Draw only specified edges

    edge_widths : float, or array of floats
       Relative Line width of edges (default=1.0). Use scalar to chat width.

    edge_scalar : float
       Scale all edges (default=1.0)

    edge_colors : color string, or array of floats
       Edge color. Can be a single color format string (default='r'),
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    edge_style : string
       Edge line style (default='solid') (solid|dashed|dotted,dashdot)

    edge_alpha : float
       The edge transparency (default=1.0)

    edge_arrows : bool, optional (default=True)
       For directed graphs, if True draw arrowheads.
       Note: Arrows will be the same color as edges.

    edge_arrowstyles : str, optional (default='-|>')
       For directed graphs, choose the style of the arrow heads.
       See :py:class: `matplotlib.patches.ArrowStyle` for more
       options.

    edge_arrowsize : int, optional (default=10)
       For directed graphs, choose the size of the arrow head head's length and
       width. See :py:class: `matplotlib.patches.FancyArrowPatch` for attribute
       `mutation_scale` for more info.

    node_list : list, optional (default G.nodes())
       Draw only specified nodes 

    node_size : scalar or array, optional (default=300)
       Size of nodes.  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats, (default=phenotypes)
       Node color. Can be a single color format string,
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string, optional (default='o')
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8'.

    node_alpha : float, optional (default=1.0)
       The node and edge transparency

    node_linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    node_edgecolors: "black"

    cmap : Matplotlib colormap, optional (default='plasmas')
       Colormap for mapping intensities of nodes

    cmap_truncate : bool
        Use only a subspace of the color map spectrum. If False whole color spectrum (0 to 1) is used.

    cmap_max : float (default=0.95)
        Upper bound of the color spectrum.

    cmap_min : float (default=0.05)
        Lower bound of the color spectrum.

    colorbar : False
        If True, show colorbar for nodes.

    vmin,vmax : float, optional (default=None)
       Minimum and maximum for node colormap scaling

    Notes
    -----
    For directed graphs, "arrows" (actually just thicker stubs) are drawn
    at the head end.  Arrows can be turned off with keyword arrows=False.
    Yes, it is ugly but drawing proper arrows with Matplotlib this
    way is tricky.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        despine(ax)
    else:
        fig = ax.get_figure()

    # Flattened positions
    pos = flattened(G, vertical=True)

    # Style and draw edges
    if edge_list is None:
        edge_list = list(G.edges().keys())

    edge_options = dict(
        edge_list=edge_list,
        widths=edge_widths,
        scalar=edge_scalar,
        colors=edge_colors,
        style=edge_style,
        alpha=edge_alpha,
        arrows=edge_arrows,
        arrowstyles=edge_arrowstyles,
        arrowsize=edge_arrowsize
    )

    draw_edges(G, pos, ax=ax, **edge_options)

    # Style and draw nodes
    if node_list is None:
        node_list = list(G.nodes().keys()) 

    node_options = dict(
        node_list=node_list, 
        size=node_size,
        color=node_color,
        shape=node_shape,
        alpha=node_alpha,
        linewidths=node_linewidths,
        edgecolors=node_edgecolors,
        cmap=cmap,
        cmap_truncate=True,
        cmap_max=cmap_max,
        cmap_min=cmap_min,
        colorbar=colorbar,
        vmin=vmin,
        vmax=vmax,
    )

    draw_nodes(G, pos, ax=ax, **node_options)