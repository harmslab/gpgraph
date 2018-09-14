def get_nodes_from_attributes(G, attrs):
    """Convert any list of attributes to a index list."""
    # Get one item from list.
    attr = list(attrs)[0]

    # Find item in map attributes.
    if attr in G.gpm.index:
        return attrs

    elif attr in G.gpm.genotypes:
        map_ = G.gpm.map('genotypes', 'index')

    elif attr in G.gpm.binary:
        map_ = G.gpm.map('binary', 'index')

    idx = [map_[attr] for attr in attrs]
    return idx


def split_map(idx_list):
    """Return
    """
    return list(set(G.gpm.idx).difference(set(idx_list)))
