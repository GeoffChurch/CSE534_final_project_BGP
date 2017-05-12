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
    parser.add_argument('-r', '--resolution', required=True,
                        help='how many samples to take for density',
                        type=int)
    #parser.add_argument('-d', '--density', required=True,
    #                    help='graph density = ratio of number of edges to number of all possible edges n*(n-1)',
    #                    type=float)
    parser.add_argument('-f', '--func', required=True,
                        help='type of algorithm for graph creation.' +
                        'Choices: rand-connected-graph or rand-graph',
                        type=str)
    args = parser.parse_args()
    num_nodes = args.number
    densityExpF = lambda i : ((2**((i/(args.resolution-1))**4))-2)
    with open('out_nodes:{},res:{}.tsv'.format(num_nodes, args.resolution), 'w') as of:
        of.write('\t'.join(map(str, range(args.resolution))) + '\n')
        of.write('\t'.join(str(densityExpF(i)) for i in range(args.resolution)) + '\n\n')
        runs_per_epoch = 10
        scores = [0]*args.resolution
        for epoch in range(runs_per_epoch):
            print('\n\nepoch:', epoch)
            for i in range(args.resolution):
                densityExp = densityExpF(i)
                print('densityExp: {}\t\tedges: {}'.format(densityExp, (num_nodes*(num_nodes-1))*num_nodes**densityExp))
                g = graph.createGraph(num_nodes=num_nodes, density=num_nodes**densityExp, func=args.func)
                score = local.local(g)
                scores[i] += score
                of.write(str(score) + '\t')
                of.flush()
            of.write('\n')
            of.flush()
        scores[:] = [score / runs_per_epoch for score in scores]
        of.write('\n\n' + '\n'.join('{}\t{}'.format(densityExpF(i), scores[i]) for i in range(args.resolution)) + '\n')
        of.flush()
    # print('END STATE!')
    # for nodeName, node in sorted(nodes.items()):
    #     print(nodeName)
    #     print(node.curState())
    #     print()


