def local(G, node2rejects, node2path2score):
    src2dst2bestPath = {src: {
        dst: [] for dst in G.getNodes()
    } for src in G.getNodes()}
    node2scoreFunc
