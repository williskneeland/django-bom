# try:
#     import pygraphviz as pgv
#     using_graphviz = True
# except ImportError:
#     using_graphviz = False
#

# from anytree.exporter import DotExporter
# from os import path
# from django.conf import settings
#
# ILLEGAL_FILENAME_CHARS = '<>:"/\|?*'
#

from anytree import Node, RenderTree


def workflow_str(initial_state, forward_transitions):
    root = workflow_to_tree(initial_state, forward_transitions)

    tree_str_lines = []
    for pre, fill, node in RenderTree(root):
        tree_str_lines.append("%s%s" % (pre, node.name))

    return tree_str_lines

def workflow_to_tree(initial_state, forward_transitions):
    edges = {}
    for transition in forward_transitions:
        source = str(transition.source_state)
        target = str(transition.target_state)

        try:
            edges[source].append(target)
        except KeyError:
            edges[source] = [target]

    root = Node(name=initial_state.name, children=[])
    helper(root, edges)
    return root


def helper(cur_node, edges):
    if cur_node is None:
        return

    if cur_node.name in edges:
        for target_name in edges[cur_node.name]:
            child_node = Node(name=target_name, parent=cur_node)
            helper(child_node, edges)

            
 #
#
# def workflow_img(initial_state, forward_transitions, filename, dir):
#     if not using_graphviz:
#         return False
#
#     root = workflow_to_tree(initial_state, forward_transitions)
#     filename = filename.strip(ILLEGAL_FILENAME_CHARS).replace(" ", '') + '.png'
#     if len(dir) > 0:
#         dir += '/'
#     full_path = dir+filename
#     if path.exists(full_path):
#         return filename
#     else: # diagram doesn't exist, try to create it
#         try:
#             DotExporter(root).to_picture(full_path)
#             return filename
#         except:
#             return False
#
#
