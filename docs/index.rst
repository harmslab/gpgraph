.. gpgraph documentation master file, created by
   sphinx-quickstart on Wed May 23 21:58:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GPGraph
=======

**Genotype-phenotype maps in NetworkX**


.. code-block:: python

  from gpmap.simulate import MountFujiSimulation
  from gpgraph import GenotypePhenotypeGraph, draw_flattened

  # Simulate a genotype-phenotype map
  sim = MountFujiSimulation.from_length(4, roughness_width=1)

  # Turn the genotype-phenotype map into a networkx object
  G = GenotypePhenotypeGraph(gpm)

  # Draw the graph
  draw_flattened(G, with_labels=False, node_size=100)


.. image:: _img/readme-fig.png


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   _reference/gpgraph.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
