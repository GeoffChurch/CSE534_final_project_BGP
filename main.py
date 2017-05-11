import argparse

import graph
import local

# def main():
#     pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', required=True,
                        help='number of nodes in graph',
                        type=int)
    parser.add_argument('-d', '--density', required=True,
                        help='graph density = ratio of number of edges to number of all possible edges n*(n-1)',
                        type=float)
    parser.add_argument('-t', '--type', required=True,
                        help='type of algorithm for graph creation.' +
                        'Choices: rand-connected-graph or rand-graph',
                        type=str)
    args = parser.parse_args()
    g = graph.createGraph(args.number, args.density, args.type)
    nodes = local.local(g)
    # print('END STATE!')
    # for nodeName, node in sorted(nodes.items()):
    #     print(nodeName)
    #     print(node.curState())
    #     print()


