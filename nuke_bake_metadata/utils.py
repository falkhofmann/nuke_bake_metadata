"""Provide utility functions."""

import unicodedata

try:
    import nuke
except ImportError:
    pass

from nuke_bake_metadata.constants import COLORS


def is_number(string):
    """Check if string is numeric.

    Args:
        string (str): String to verify if numerical or not.

    Returns:
        bool: True if string is numerical.

    """
    try:
        float(string)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(string)

        return True
    except (TypeError, ValueError):
        pass


def get_value_type(node, key):
    """Seperate between text, numeric or list.

    Args:
        node (nuke.node): Node to run metadata check on.
        key (str): Metadata key.

    Returns:
        str: Text, Number or List

    """
    value = node.metadata(key)
    type_ = 'Text'
    if is_number(value):
        type_ = 'Number'

    return type_


def create_node(node):
    """Create a NoOp node with specific color, position and label.

    Args:
        node (nuke.node): Node to place next to.

    Returns:
        Node: NoOp Node.

    """
    lab = 'baked metadata\nfrom {}'.format(node.name())
    noop = nuke.nodes.NoOp(hide_input=True,
                           xpos=node.xpos() + 100,
                           ypos=node.ypos(),
                           tile_color=COLORS['noop'],
                           label=lab)
    return noop


def create_numerical_animation(node, noop, m_key, key, first, last):  # pylint: disable=too-many-arguments
    """Create a custom knob and add animation to it.

    Args:
        node (nuke.node): Node to read metadata from.
        noop (nuke.node): Node to add custom knob to.
        m_key (str): Full metadata key.
        key (str): Last section of metadata key.
        first (int): Frame number when animation should start.
        last (int): Frame number when animation should stop.

    """
    animation = nuke.Double_Knob(key)
    noop.addKnob(animation)
    animation.setAnimated()
    anim = animation.animations()[0]
    anim.addKey([nuke.AnimationKey(i, node.metadata(m_key, i)) for i in xrange(first, last)])

    nuke.show(noop)


def get_node():
    """Get the current selected node from nodegraph.

    Returns:
        Node: Selected node.

    """
    return nuke.selectedNode()


def get_metadata(node):
    """Extract all metadata keys from Node.

    Args:
        node (nuke.node): Node to read metadata from.

    Returns:
        dict: Last section of metadata key as key and full metadata key as
            value.

    """
    return {key.rpartition('/')[-1]: key for key in node.metadata().keys()}
