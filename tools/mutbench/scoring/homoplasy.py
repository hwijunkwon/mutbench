"""Fitch parsimony-based homoplasy scoring for each genomic position.

Implements the Fitch algorithm (1971) to count the minimum number of
character state changes at each alignment position on a phylogenetic tree.
Positions with high parsimony counts indicate convergent/parallel evolution
(homoplasy), suggesting functional constraint or positive selection.
"""

import numpy as np
from Bio import Phylo
from io import StringIO


def _get_terminals_map(tree):
    """Map terminal clade names to their index in the tree's terminal list."""
    terminals = tree.get_terminals()
    return {t.name: i for i, t in enumerate(terminals)}


def fitch_parsimony_count(tree, alignment_dict, seq_length):
    """
    For each position in the alignment, count the minimum number of
    state changes (mutations) on the phylogenetic tree using Fitch parsimony.

    Args:
        tree: Bio.Phylo tree object
        alignment_dict: dict mapping sequence name -> sequence string
        seq_length: length of (truncated) alignment

    Returns:
        numpy array of shape (seq_length,) with per-position mutation counts
    """
    counts = np.zeros(seq_length, dtype=int)

    # Pre-build terminal name -> sequence lookup
    terminal_names = {t.name for t in tree.get_terminals()}
    # Filter alignment to only terminals present in tree
    valid_names = terminal_names & set(alignment_dict.keys())
    if len(valid_names) < 3:
        return counts

    # Process each position independently
    for pos in range(seq_length):
        changes = _fitch_single_position(tree.root, alignment_dict, pos, valid_names)
        counts[pos] = changes

    return counts


def _fitch_single_position(root, alignment_dict, pos, valid_names):
    """Run Fitch algorithm for a single alignment position.

    Bottom-up pass: compute intersection/union of child state sets.
    Count a change each time intersection is empty (union is taken).

    Returns: minimum number of state changes at this position.
    """
    changes = 0
    # Cache for state sets at each clade (use id as key)
    state_sets = {}

    # Post-order traversal (bottom-up)
    for clade in root.find_elements(order='postorder'):
        if clade.is_terminal():
            # Leaf node: state set is the observed character
            name = clade.name
            if name in valid_names:
                char = alignment_dict[name][pos]
                if char in ('-', 'X', 'J', 'B', 'Z', '*', '.'):
                    # Ambiguous or gap: treat as wildcard (all states)
                    state_sets[id(clade)] = None  # None = wildcard
                else:
                    state_sets[id(clade)] = {char}
            else:
                state_sets[id(clade)] = None  # Missing: wildcard
        else:
            # Internal node: intersect/union of children
            child_sets = []
            for child in clade.clades:
                cid = id(child)
                if cid in state_sets:
                    child_sets.append(state_sets[cid])

            if not child_sets:
                state_sets[id(clade)] = None
                continue

            # Filter out wildcards
            non_wildcard = [s for s in child_sets if s is not None]
            if not non_wildcard:
                state_sets[id(clade)] = None
                continue

            # Fitch rule: intersect all children
            result = non_wildcard[0].copy()
            for s in non_wildcard[1:]:
                inter = result & s
                if inter:
                    result = inter
                else:
                    # No intersection -> take union, count a change
                    result = result | s
                    changes += 1

            state_sets[id(clade)] = result

    return changes


def load_tree(tree_path):
    """Load a Newick tree from file."""
    return Phylo.read(tree_path, 'newick')


def load_tree_from_string(newick_str):
    """Load a Newick tree from string."""
    return Phylo.read(StringIO(newick_str), 'newick')
