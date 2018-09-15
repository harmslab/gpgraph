
from collections import Counter
import networkx as nx

def forward_paths(G, source, target):
    """Return all forward paths from source genotype to
    target genotype.

    Returns
    -------
    paths : List of path
        Will always return a list of paths labeled by their node index.
    """
    from .base import GenotypePhenotypeGraph

    if not isinstance(G, GenotypePhenotypeGraph):
        raise Exception("G must be a GenotypePhenotypeGraph.")

    # Get source and target from G. Is it genotype, binary, or node number
    if source in G.gpm.index:
        pass

    elif source in G.gpm.genotypes:
        series = list(G.gpm.genotypes)
        source = series.index(source)
        target = series.index(target)

    elif source in G.gpm.binary:
        series = list(G.gpm.binary)
        source = series.index(source)
        target = series.index(target)

    paths = nx.all_shortest_paths(G, source=source, target=target)
    return list(paths)


def forward_paths_prob(G, source, target):
    """Find forward paths and calculate their probability.
    """
    paths = forward_paths(G, source, target)

    path_prob = {}
    for path in paths:
        p = 1
        for i in range(len(path)-1):
            edge = (path[i], path[i+1])
            p *= G.edges[edge]["prob"]
        path_prob[tuple(path)] = p

    return path_prob


def paths_to_edges(paths, repeat=False):
    """Chops a list of paths into its edges.

    Parameters
    ----------
    paths: list of tuples
        list of the paths.

    repeat: bool (False)
        include edges repeats?

    Returns
    -------
    edges: list
        List of edges
    """
    edges = []
    for path in paths:
        edges += [(path[i], path[i+1]) for i in range(len(path)-1)]

    # Return a list of edges with repeats
    if repeat:
        return edges

    # Else remove repeats
    else:
        return list(set(edges))


def paths_to_edges_count(paths):
    """Chops a list of paths into its edges, counting each edge visited.

    Parameters
    ----------
    paths: list of tuples
        list of the paths.

    Returns
    -------
    edges: Counter dictionary
        Edge tuples as keys, and counts as values.
    """
    edges = paths_to_edges(paths, repeat=True)
    return Counter(edges)


def paths_prob_to_edges_flux(paths_prob):
    """Chops a list of paths into its edges, and calculate the probability
    of that edge across all paths.

    Parameters
    ----------
    paths: list of tuples
        list of the paths.

    Returns
    -------
    edge_flux: dictionary
        Edge tuples as keys, and probabilities as values.
    """
    edge_flux = {}
    for path, prob in paths_prob.items():

        for i in range(len(path)-1):
            # Get edge
            edge = (path[i], path[i+1])

            # Get path probability to edge.
            if edge in edge_flux:
                edge_flux[edge] += prob

            # Else start at zero
            else:
                edge_flux[edge] = prob

    return edge_flux


def edges_flux_to_node_flux(G):
    """Sum all flux from incoming edges for each node"""
    node_fluxes = {}
    for node in G.nodes:
        node_flux = sum([edge[2] for edge in list(G.in_edges(node, data="capacity")) if edge[2]])
        node_fluxes[node] = node_flux
    return node_fluxes
