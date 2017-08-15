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

### Add an evolutionary model

```python

def adaptive(fitness1, fitness2):
    if fitness2 > fitness1:
        return 0
    else:
        return 1

G = GenotypePhenotypeGraph(gpm)
G.add_evolutionary_model(adaptive)
```

### Draw
