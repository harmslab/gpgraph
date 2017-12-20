# GPGraph: NetworkX graphs for genotype-phenotype maps

Port a `GenotypePhenotypeMap` to [NetworkX's Digraph](https://networkx.github.io/).

## Installation

Clone this repo and install with `pip`:

```
pip install -e .
```

## Basic Usage

###  Initialize a network

```python

import networkx as nx

gpm = GenotypePhenotypeMap.from_json("data.json")
G = GenotypePhenotypeGraph(gpm)

nx.draw(G)
```
