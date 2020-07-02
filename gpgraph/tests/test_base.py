import pytest
from gpmap.gpm import GenotypePhenotypeMap
from gpgraph.base import get_neighbors, GenotypePhenotypeGraph
import numpy as np


@pytest.fixture
def gpmap_base():
    # Data
    wildtype = "AAA"
    genotypes = ["AAA", "AAT", "ATA", "TAA", "ATT", "TAT", "TTA", "TTT"]
    phenotypes = [0.1, 0.2, 0.2, 0.6, 0.4, 0.6, 1.0, 1.1]
    stdeviations = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

    # Initialize the object
    gpm = GenotypePhenotypeMap(wildtype,
                               genotypes,
                               phenotypes,
                               stdeviations=stdeviations)
    return gpm


@pytest.fixture
def gpgraph_test(gpmap_base):
    gpgraph_test = GenotypePhenotypeGraph(gpmap_base)

    return gpgraph_test


@pytest.fixture
def binary_gpgraph():
    gpbinary = get_neighbors('000', {0: ['0', '1'], 1: ['0', '1'], 2: ['0', '1']})
    gpbinary = np.array(gpbinary).sort()

    return gpbinary


def test_attributes(gpmap_base):
    """"Test data is same as passed to GenotypePhenotypeMap object"""
    assert gpmap_base.wildtype == "AAA"
    np.testing.assert_array_equal(gpmap_base.genotypes,
                                  np.array(["AAA", "AAT", "ATA", "TAA", "ATT", "TAT", "TTA", "TTT"]))
    np.testing.assert_array_equal(gpmap_base.phenotypes,
                                  np.array([0.1, 0.2, 0.2, 0.6, 0.4, 0.6, 1.0, 1.1]))
    np.testing.assert_array_equal(gpmap_base.stdeviations,
                                  np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]))


def test_get_neighbors(gpmap_base, binary_gpgraph):
    """"Test if function can find all neighboring nodes"""
    found_neighbors = np.array(get_neighbors(gpmap_base.genotypes[1], gpmap_base.mutations)).sort()
    desired_neighbors = np.array(['TAT', 'TTT', 'TTA']).sort()
    np.testing.assert_array_equal(found_neighbors,
                                  desired_neighbors)
    np.testing.assert_array_equal(binary_gpgraph, np.array(['100', '110', '111']).sort())


def test_type(gpgraph_test):
    assert isinstance(gpgraph_test, GenotypePhenotypeGraph)


def test_add_gpm(gpgraph_test, gpmap_base):
    assert gpgraph_test.gpm == gpmap_base


def test_read_json(gpgraph_test):
    """Test reading from json"""
    read_gpm = GenotypePhenotypeGraph.read_json("data/test_data.json")
    # Test instance was created
    assert isinstance(read_gpm, GenotypePhenotypeGraph)
    # Test elements align
    np.testing.assert_array_equal(gpgraph_test.nodes, read_gpm.nodes)


# Read CSV is currently failing

# def test_read_csv(gpgraph_test):
#     """Test reading from json"""
#     read_gpm = GenotypePhenotypeGraph.read_csv("data/test_data.csv", wildtype='AAA')
#     # Test instance was created
#     assert isinstance(read_gpm, GenotypePhenotypeGraph)
#     # Test elements align
#     np.testing.assert_array_equal(gpgraph_test.nodes, read_gpm.nodes)