# GPGraph

[![PyPI version](https://badge.fury.io/py/gpgraph.svg)](https://badge.fury.io/py/gpgraph)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/harmslab/gpgraph/blob/master/examples/Introduction_to_gpgraph.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/harmslab/gpvolve.git/master?filepath=examples%2FIntroduction%20to%20gpvolve.ipynb)

**Genotype-phenotype maps in NetworkX**

Port a `GenotypePhenotypeMap` to a [NetworkX Digraph](https://networkx.github.io/).

## Basic Example

GPGraph follows NetworkX syntax. Initialize a graph, add the
genotype-phenotype map object, and draw the graph. This library even
comes with a draw method, `draw_gpgraph`, suited for genotype-phenotype graphs.

```python
from gpmap.simulate import MountFujiSimulation

from gpgraph import GenotypePhenotypeGraph
from gpgraph.pyplot import draw_gpgraph

# Simulate a genotype-phenotype map
sim = MountFujiSimulation.from_length(4, roughness_width=1)

# Turn the genotype-phenotype map into a networkx object
G = GenotypePhenotypeGraph(sim)

# Draw the graph
figure = draw_gpgraph(G,
                      edge_colors = 'gray', 
                      node_size=400)
```
<img src="https://raw.githubusercontent.com/harmslab/gpgraph/master/docs/_img/readme-fig.png" width="350">


## Install

Clone this repo and install with `pip`:

```
pip install -e .
```

## To develop

Clone this repo and run `setup.py` as follows

```
python setup.py develop --user
```

This way, if only python scripts are being changed nothing has
to be reinstalled.
