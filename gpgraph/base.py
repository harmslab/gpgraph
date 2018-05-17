import numpy as np
import networkx as nx
from .draw import draw_flattened

def get_neighbors(genotype, mutations):
    """Return all genotypes

    Parameters
    ----------
    genotype : str
        reference genotype.
    mutations : dict
        mutations dictionary from a genotype-phenotype map.

    Returns
    -------
    neighbors : tuple
        tuple of neighbors.
    """
    neighbors = tuple()
    for i, char in enumerate(genotype):
        # Copy reference genotype
        genotype2 = list(genotype)[:]

        # Find possible mutations at site i.
        options = mutations[i][:]
        options.remove(char)

        # Construct neighbor genotypes.
        for j in options:
            genotype2[i] = j
            genotype2_ = "".join(genotype2)
            neighbors += (genotype2_,)
    return neighbors


class GenotypePhenotypeGraph(nx.DiGraph):
    """Construct a NetworkX DiGraph object from a GenotypePhenotypeMap."""
    def __init__(self, gpm=None, *args, **kwargs):
        super(GenotypePhenotypeGraph, self).__init__(*args, **kwargs)
        self.add_gpm(gpm)

    def add_gpm(self, gpm):
        """Attach a Network DiGraph to GenotypePhenotypeMap object."""
        # Add gpm
        self.gpm = gpm
        data = self.gpm.data

        # genotypes to index.
        m = dict(zip(data.genotypes, data.index))

        # Iterate through nodes.
        edges = []
        for i in data.index:
            # Add node to graph
            row = data.loc[i]
            self.add_node(i, **row)

            # Get edges from node.
            neighbors = get_neighbors(row['genotypes'], self.gpm.mutations)
            for neighbor in neighbors:
                # Check if node is in data.
                if neighbor in m:
                    j = m[neighbor]
                    edges.append((i, j))

        # Add edges to network
        self.add_edges_from(edges)

    def __repr__(self):
        draw_flattened(self)
        return super(GenotypePhenotypeGraph, self).__repr__()
