import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from gpgraph.paths import paths_prob_to_edges_flux, forward_paths_prob
from gpgraph.pyplot.pos import flattened

from .utils import despine


def draw_paths(
        G,
        paths=None,
        pos=None,
        edge_list=None,
        source=None,
        target=None,
        edge_equal=False,
        edge_scalar=1.0,
        edge_color='k',
        width=1.0,
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
        cmap_truncate=False,
        cmap_max=0.95,
        cmap_min=0.05,
        vmin=None,
        vmax=None,
        ax=None,
        linewidths=0,
        edgecolors="black",
        label=None,
        colorbar=False,
):
    """Draw paths in GenotypePhenotypeGraph

    Parameters
    ----------
    G : graph
       A networkx graph

    paths : All forward paths from source genotype to
        target genotype.

    source: source genotype. Default value is the first value
        in the list of genotypes.

    target: target genotype. Default value is the last value
        in the list of genotypes.

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.
       Default value uses flattened function included in gpgraph.utils.

    edge_list : collection of edge tuples
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

    cmap_truncate : bool
        Use only a subspace of the color map spectrum. If False whole color spectrum (0 to 1) is used.

    cmap_min : float (default=0.05)
        Lower bound of the color spectrum.

    cmap_max : float (default=0.95)
        Upper bound of the color spectrum.

    edge_cmap : Matplotlib colormap
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
    # Check what values were passed to function, or assign default values
    if not pos:
        pos = flattened(G)

    if not edge_list:
        edge_list = G.edges()

    if not nodelist:
        nodelist = G.nodes()

    if not source:
        source = G.gpm.genotypes[0]

    if not target:
        target = G.gpm.genotypes[-1]

    if not paths:
        paths = forward_paths_prob(G, source, target)

    # Get Figure.
    if ax is None:
        fig, ax = plt.subplots()
        despine(ax)
    else:
        fig = ax.get_figure()

    # Get flux through edges
    edges = paths_prob_to_edges_flux(paths)
    edge_list = list(edges.keys())

    # Default options
    node_options = dict(
        nodelist=G.nodes(),
        vmin=vmin,
        vmax=vmax,
        node_shape=node_shape,
        node_size=node_size,
        node_color=[G.nodes[n]['phenotypes'] for n in nodelist],
        linewidths=linewidths,
        edgecolors=edgecolors,
        cmap=cmap,
        cmap_truncate=False,
        labels={n: G.nodes[n]['genotypes'] for n in nodelist}
    )

    # Draw edges
    nx.draw_networkx_edges(
        G=G,
        pos=pos,
        edgelist=edge_list,
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

    # Add a color bar
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)

        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)
