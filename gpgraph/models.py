import numpy as np

def strong_selection_weak_mutation(fitness1, fitness2):
    """Strong selection, weak mutation model."""
    sij = (fitness2 - fitness1) / fitness1
    if sij < 0:
        sij = 0
    return 1 - np.exp(-sij)
