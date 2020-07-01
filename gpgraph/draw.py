import matplotlib as mpl
import matplotlib.colors as colors
from gpgraph.pyplot.utils import truncate_colormap
from matplotlib import pyplot as plt
from gpgraph.pyplot import flattened
import networkx as nx


def draw_flattened(
        G,
        ax=None,
        nodelist=[],
        node_attribute="phenotypes",
        vmin=None,
        vmax=None,
        cmap='plasma',
        cmap_truncate=False,
        cmap_max=0.95,
        cmap_min=0.05,
        colorbar=False,
        labels='binary',
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
    node_attribute : string (default = "phenotypes")
       node attribute that is used to set the color
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
    cmap_truncate : bool
        Use only a subspace of the color map spectrum. If False whole color spectrum (0 to 1) is used.
    cmap_min : float (default=0.05)
        Lower bound of the color spectrum.
    cmap_max : float (default=0.95)
        Upper bound of the color spectrum.
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
        attributes = list(nx.get_node_attributes(G, name=node_attribute).values())
        vmin = min(attributes)
        vmax = max(attributes)
    if cmap_truncate:
        cmap = truncate_colormap(cmap, minval=cmap_min, maxval=cmap_max)

    # Default options
    options = dict(
        pos=pos,
        nodelist=nodelist,
        arrows=False,
        vmin=vmin,
        vmax=vmax,
        node_color=[G.nodes[n][node_attribute] for n in nodelist],
        cmap=cmap,
        cmap_truncate=False,
        edge_color='gray',
        labels={n: G.nodes[n][labels] for n in nodelist}
    )
    options.update(**kwds)

    # Draw fig
    nx.draw_networkx(G, **options)

    # Add a color bar
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)
        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)
