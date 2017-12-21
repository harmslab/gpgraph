import numpy as np
import networkx as nx


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
            genotype2 = "".join(genotype2)
            neighbors += (genotype2,)
    return neighbors


class GenotypePhenotypeGraph(nx.DiGraph):
    """Construct a NetworkX DiGraph object from a GenotypePhenotypeMap."""

    def add_gpm(self, gpm, genotypes='complete'):
        """Attach a Network DiGraph to GenotypePhenotypeMap object."""
        # Add gpm
        self.gpm = gpm

        # Iterate through known genotypes.
        if genotypes == 'complete':
            data = self.gpm.complete_data
        elif genotypes == 'obs':
            data = self.gpm.data
        else:
            raise Exception("genotypes keyword argument must be "
                            "`complete` or `obs`.")

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
