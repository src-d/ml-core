from distutils.version import StrictVersion
from typing import List, Sequence

from bblfsh.compat import CompatBblfshClient as BblfshClient
from bblfsh.compat import CompatNodeIterator, Node


BBLFSH_VERSION_LOW = "3.0"
BBLFSH_VERSION_HIGH = "4.0"


def check_version(host: str = "0.0.0.0", port: str = "9432") -> bool:
    """
    Check if the bblfsh server version matches module requirements.

    :param host: bblfsh server host.
    :param port: bblfsh server port.
    :return: True if bblfsh version specified matches requirements.
    """
    # get version and remove leading 'v'
    version = StrictVersion(BblfshClient("%s:%s" % (host, port)).version().version.lstrip("v"))
    return StrictVersion(BBLFSH_VERSION_LOW) <= version < StrictVersion(BBLFSH_VERSION_HIGH)


def iterate_children(nodes: Sequence[Node]) -> CompatNodeIterator:
    """
    Use this function to access the node.children attribute in a Babelfish v3 Node.

    By default, node.children return the children of the nodes as Node objects or as dicts, but
    Babelfish v2 returns only Node instances. This function adapts the returned bblfsh v3 children
    to return only Node instances.

    The node.children attribute is transformed to an iterator, and then filtered by a
    CompatNodeIterator. The CompatNodeIterator transforms the dict nodes into Node instances.
    """
    def node_generator(node_seq):
        for val in node_seq:
            yield val
    return CompatNodeIterator(node_generator(nodes))


def get_node_tokens(node: Node) -> List[str]:
    """
    Return the node.token attribute from a Babelfish v3 Node.

    The token attribute is supposed to return a string, but given that several of \
     them are found inside every Node, this function returns a list containing them all.
    """
    return (ident["boxed_value"]["Name"] for ident in node.get_dict().get("identifiers", []))


def get_node_start_line(node: Node) -> dict:
    """
    Return the node.start_line  attribute from a Babelfish v3 Node.

    Directly accessing the attribute will cause the program to crash due to improper checking of
    missing values. This function aims to correct this and will return

    :param node: Target node.
    :return: A dict containing node.start_line in case it exists or an empty dictionary in case \
             it does not exist.
    """
    nd = node.get_dict()
    if "@pos" in nd.keys():
        return nd["@pos"].get("start", {})
    return {}
