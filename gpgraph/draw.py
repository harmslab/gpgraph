import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from .paths import paths_prob_to_edges_flux

def flattened(G, scale=1, vertical=False):
    """Get flattened positions for a genotype-phenotype graph.

    Parameters
    ----------
    G : GenotypePhenotypeGraph object
        A genotype-phenotype objects
    scale : float (default=1)
        density of the nodes.

    Returns
    -------
    positions: dict
        positions of all nodes in network (i.e. {index: [x,y]})
    """
    # Get the binary genotypes from GPM
    # Set level of nodes and begin calc offset on the fly
    graph = G
    offsets = {}
    positions = {}
    for n in range(len(list(G.nodes()))):
        node = graph.node[n]
        # Calculate the level of each node
        level = node["binary"].count("1")
        if level in offsets:
            offsets[level] += 1
        else:
            offsets[level] = 1
        positions[n] = [level]
    # Center the offsets on 0
    for key, val in offsets.items():
        offsets[key] = list(np.arange(val) - (val-1)/2.0)
    # Offset positions
    if vertical:
        for n in range(len(list(G.nodes()))):

            pos = offsets[positions[n][0]].pop(0)
            scaled = scale*pos
            positions[n].insert(0, scaled)
            positions[n][-1] *= -1
    else:
        for n in range(len(list(G.nodes()))):

            pos = offsets[positions[n][0]].pop(0)
            scaled = scale*pos
            positions[n].append(scaled)
    return positions


def draw_flattened(
    G,
    ax=None,
    nodelist=[],
    vmin=None,
    vmax=None,
    cmap='plasma',
    colorbar=False,
    **kwds):
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

    arrows : bool, optional (default=False)
       For directed graphs, if True draw arrowheads.

    with_labels :  bool, optional (default=True)
       Set to True to draw labels on the nodes.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional (default G.nodes())
       Draw only specified nodes

    edgelist : list, optional (default=G.edges())
       Draw only specified edges

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

    alpha : float, optional (default=1.0)
       The node and edge transparency

    cmap : Matplotlib colormap, optional (default='plasmas')
       Colormap for mapping intensities of nodes

    vmin,vmax : float, optional (default=None)
       Minimum and maximum for node colormap scaling

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    width : float, optional (default=1.0)
       Line width of edges

    color_bar : False
        If True, show colorbar for nodes.

    edge_color : color string, or array of floats (default='gray')
       Edge color. Can be a single color format string,
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    edge_cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of edges

    edge_vmin,edge_vmax : floats, optional (default=None)
       Minimum and maximum for edge colormap scaling

    style : string, optional (default='solid')
       Edge line style (solid|dashed|dotted,dashdot)

    labels : dictionary, optional (default='genotypes')
       Node labels in a dictionary keyed by node of text labels

    font_size : int, optional (default=12)
       Font size for text labels

    font_color : string, optional (default='k' black)
       Font color string

    font_weight : string, optional (default='normal')
       Font weight

    font_family : string, optional (default='sans-serif')
       Font family

    label : string, optional
        Label for graph legend

    Notes
    -----
    For directed graphs, "arrows" (actually just thicker stubs) are drawn
    at the head end.  Arrows can be turned off with keyword arrows=False.
    Yes, it is ugly but drawing proper arrows with Matplotlib this
    way is tricky.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Flattened position
    pos = flattened(G, vertical=True)

    if not nodelist:
        nodelist = list(G.nodes().keys())

    if vmax is None:
        phenotypes = G.gpm.phenotypes
        vmin = min(phenotypes)
        vmax = max(phenotypes)

    # Default options
    options = dict(
        pos=pos,
        nodelist=nodelist,
        arrows=False,
        vmin=vmin,
        vmax=vmax,
        node_color=[G.nodes[n]['phenotypes'] for n in nodelist],
        cmap=cmap,
        edge_color='gray',
        labels={n: G.nodes[n]['genotypes'] for n in nodelist}
    )
    options.update(**kwds)

    # Draw fig
    nx.draw_networkx(G, **options)

    # Add a colorbar?
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)

        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)

def draw_paths(
    G,
    paths,
    pos=None,
    edge_equal=False,
    edge_scalar=1.0,
    edge_color='k',
    style='solid',
    edge_alpha=1.0,
    arrows=False,
    arrowstyle='-|>',
    arrowsize=10,
    nodelist=None,
    node_size=300,
    node_color='r',
    node_shape='o',
    alpha=1.0,
    cmap='plasma',
    vmin=None,
    vmax=None,
    ax=None,
    linewidths=None,
    edgecolors=None,
    label=None,
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

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Get positions of nodes.
    if pos is None:
        pos = flattened(G, vertical=True)

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

    if not nodelist:
        nodelist = list(G.nodes().keys())

    if vmax is None:
        phenotypes = G.gpm.phenotypes
        vmin = min(phenotypes)
        vmax = max(phenotypes)

    # Default options
    node_options = dict(
        nodelist=nodelist,
        vmin=vmin,
        vmax=vmax,
        node_size=node_size,
        node_color=[G.nodes[n]['phenotypes'] for n in nodelist],
        cmap=cmap,
        labels={n: G.nodes[n]['genotypes'] for n in nodelist}
    )

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

    # Draw nodes.
    nx.draw_networkx_nodes(
        G=G,
        pos=pos,
        ax=ax,
        **node_options
    )
