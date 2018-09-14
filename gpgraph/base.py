import numpy as np
import networkx as nx
from .draw import draw_flattened
from .models import strong_selection_weak_mutation
from gpmap import GenotypePhenotypeMap

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
        if mutations[i] is not None:
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
    def __init__(self, gpm, *args, **kwargs):
        super(GenotypePhenotypeGraph, self).__init__(*args, **kwargs)
        self.add_gpm(gpm)

    def __repr__(self):
        draw_flattened(self)
        return super(GenotypePhenotypeGraph, self).__repr__()

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

    def add_model(self, model=strong_selection_weak_mutation, **params):
        """Add a transition model to the edges."""
        # Add model to class.
        self.model = staticmethod(model)

        for edge in self.edges():
            node1 = edge[0]
            node2 = edge[1]

            phenotype1 = self.gpm.phenotypes[node1]
            phenotype2 = self.gpm.phenotypes[node2]

            self.edges[edge]['prob'] = model(phenotype1, phenotype2, **params)

    @classmethod
    def read_json(cls, fname):
        """Read graph from json file."""
        gpm = GenotypePhenotypeMap.read_json(fname)
        return cls(gpm)

    @classmethod
    def read_csv(cls, fname, wildtype, mutations=None):
        """Read graph from csv file."""
        gpm = GenotypePhenotypeMap.read_json(
            fname,
            wildtype=wildtype,
            mutations=mutations
        )
        return cls(gpm)
