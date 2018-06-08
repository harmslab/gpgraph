from .utils import get_nodes_from_attributes

def get_node_options(
    G, pos, nodelist=None,
    vmin=None,
    vmax=None,
    cmap='plasma',
    colorbar=False,
    node_size=300,
    **kwds
    ):
    """
    Parameters
    ----------

    G : graph
       A GenotypePhenotypeGraph.

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

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
        node_size=node_size,
    )
    colored_options.update(**kwds)

    # Options for missing nodes
    missing_options = dict(
        pos=pos,
        nodelist=missing_nodelist,
        node_color=['white' for n in missing_nodelist],
        linewidths=1.0,
        edgecolors='k',
        node_size=node_size,
    )

    return colored_options, missing_options
