"""Draws function call relationships like unix "tree" command.

    from https://stackoverflow.com/questions/32151776/visualize-tree-in-bash-like-the-output-of-unix-tree
    >>> text='''apple: banana eggplant
    banana: cantaloupe durian
    eggplant:
    fig:'''
    >>> draw_tree(parser(text))
    ├─ apple
    |  ├─ banana
    |  |  ├─ cantaloupe
    |  |  └─ durian
    |  └─ eggplant
    └─ fig
"""

import logging
from functools import reduce

LOG = logging.getLogger(__name__)

branch = "├"
pipe = "|"
end = "└"
dash = "─"


class Tree(object):
    def __init__(self, tag):
        """
        Initialize the Tree object.

        Args:
            tag (str): The tag associated with the tree node.
        """
        self.tag = tag


class Node(Tree):
    def __init__(self, tag, *nodes):
        """
        Initialize the Node object.

        Args:
            tag (str): The tag associated with the node.
            *nodes (list): List of child nodes.
        """
        super(Node, self).__init__(tag)
        self.nodes = list(nodes)


class Leaf(Tree):
    pass


def _int_draw_tree(tree, level, last=False, sup=None):
    """
    Internal function to draw the tree.

    Args:
        tree (Tree): The tree to draw.
        level (int): The current level in the tree.
        last (bool, optional): If True, this is the last node at this level of the tree. Defaults to False.
        sup (list, optional): List of levels that are "open" (i.e., have a child node). Defaults to [].

    Returns:
        list: List of strings representing the drawn tree.
    """
    if sup is None:
        sup = []

    def update(left, idx):
        """
        Update the specified index of the 'left' list with spaces.

        Args:
            left (list): The list to be updated.
            idx (int): The index in the list to be updated.

        Returns:
            list: The updated list.
        """
        if idx < len(left):
            left[idx] = "   "
        return left

    drawing = (
        "".join(reduce(update, sup, ["{}  ".format(pipe)] * level))
        + (end if last else branch)
        + "{} ".format(dash)
        + str(tree.tag)
    )
    # print("0", drawing)
    GLOBAL_LINE_HOLDER.append(drawing)

    if isinstance(tree, Node):
        level += 1
        for node in tree.nodes[:-1]:
            _int_draw_tree(node, level, sup=sup)
        _int_draw_tree(tree.nodes[-1], level, True, [level] + sup)

    return GLOBAL_LINE_HOLDER


class Track(object):
    def __init__(self, parent, idx):
        """
        Initialize the Track object.

        Args:
            parent (Node): The parent node.
            idx (int): The index of this track.
        """
        self.parent, self.idx = parent, idx


def parser(text):
    """
    Parse the given text into a list of trees.

    Args:
        text (str): The text to parse.

    Returns:
        list: The list of trees parsed from the text.
    """
    trees = []
    tracks = {}
    for line in text.splitlines():
        line = line.strip()
        key, value = map(lambda s: s.strip(), line.split(":", 1))
        # print("x", key, value, type(value))
        # sys.exit(0)
        nodes = value.split()
        if len(nodes):
            parent = Node(key)
            for i, node in enumerate(nodes):
                tracks[node] = Track(parent, i)
                parent.nodes.append(Leaf(node))
            curnode = parent
            if curnode.tag in tracks:
                t = tracks[curnode.tag]
                t.parent.nodes[t.idx] = curnode
            else:
                trees.append(curnode)
        else:
            curnode = Leaf(key)
            if curnode.tag in tracks:
                # well, how you want to handle it?
                pass  # ignore
            else:
                trees.append(curnode)
    return trees


def draw_tree(trees):
    """
    Draw the given trees and return the resulting string.

    Args:
        trees (list): The list of trees to draw.

    Returns:
        str: The string representation of the drawn trees.
    """
    global GLOBAL_LINE_HOLDER
    GLOBAL_LINE_HOLDER = []

    for tree in trees[:-1]:
        _int_draw_tree(tree, 0)
    line_list = _int_draw_tree(trees[-1], 0, True, [0])

    LOG.debug("line_list: %s", line_list)
    full_ml_tree_str = "\n".join(line_list)
    LOG.debug("full_ml_tree_str\n%s", full_ml_tree_str)

    return full_ml_tree_str


if __name__ == "__main__":
    text = """apple: banana eggplant
    banana: cantaloupe durian
    eggplant:
    fig:"""

    # text = """ghf: hist_nlines grep_history _unique_history _fakecheese
    # grep_history: porky pies
    # _unique_history: _chop_first_column _add_line_numbers _top_ten
    # _add_line_numbers: yabba dabba doo
    # histdeln: histdel
    # _fakecheese: histdel _bacon
    # _bacon: _unique_history mayo"""

    tester = draw_tree(parser(text))

    print("\ntester\n", tester)
