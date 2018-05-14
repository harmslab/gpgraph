import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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


def draw_flattened(G, ax=None, nodelist=[], **kwds):
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

    # Default options
    options = dict(
        pos=pos,
        nodelist=nodelist,
        arrows=False,
        node_color=[G.nodes[n]['phenotypes'] for n in nodelist],
        cmap='plasma',
        edge_color='gray',
        labels={n: G.nodes[n]['genotypes'] for n in nodelist}
    )


    options.update(**kwds)
    return nx.draw_networkx(G, **options)
