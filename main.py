import argparse

import graph
import local

# def main():
#     pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number',
                        help='number of nodes in graph',
                        type=int)
    parser.add_argument('-p', '--probability',
                        help='probability that any two nodes are connected',
                        type=float)
    parser.add_argument('-t', '--type',
                        help='type of algorithm for graph creation.' +
                        'Choices: rand-connected-grapg or rand-degree',
                        type=str)
    args = parser.parse_args()
    g = graph.createGraph(args.number, args.probability, args.type)
    nodes = local.local(g)
    # print('END STATE!')
    # for nodeName, node in sorted(nodes.items()):
    #     print(nodeName)
    #     print(node.curState())
    #     print()


