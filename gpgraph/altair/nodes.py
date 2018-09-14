import numpy as np
import altair as alt
import nx_altair as nxa

from .utils import despine
from gpgraph.draw.utils import get_nodes_from_attributes
from gpgraph.draw.nodes import get_node_options

def draw_map_nodes(
    G,
    pos,
    ax=None,
    nodelist=None,
    vmin=None,
    vmax=None,
    cmap='plasma',
    colorbar=False,
    node_size=300,
    node_color='phenotypes',
    **kwds):
    """Draw the nodes GenotypePhenotypeGraph.

    By specifying a nodelist, remainder nodes are drawn as empty (white) nodes.

    Parameters
    ----------
    G : graph
       A GenotypePhenotypeGraph.

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional
       Draw specified nodes (default G.nodes()) with colors, and other nodes
       as white nodes.

    node_size : scalar or array
       Size of nodes (default=300).  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats
       Node color. Can be a single color format string (default='r'),
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8' (default='o').

    alpha : float
       The node transparency (default=1.0)

    cmap : Matplotlib colormap
       Colormap for mapping intensities of nodes (default=None)

    vmin,vmax : floats
       Minimum and maximum for node colormap scaling (default=None)

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    """
    colored_options, missing_options = get_node_options(
        G, pos, nodelist=nodelist,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        node_size=node_size,
        node_color=node_color,
        **kwds
    )

    viz = nxa.draw_networkx_nodes(G, **colored_options)
    if missing_options['nodelist'] == []:
        return despine(viz)

    viz2 = nxa.draw_networkx_nodes(G, **missing_options)
    return  viz + viz2
