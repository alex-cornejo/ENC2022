import matplotlib.pyplot as plt
import networkx as nx


def print_graph(points, tour, cost):
    tour_color = "blue"
    G = nx.Graph()
    
    for i in range(0, len(tour) - 1):
        v = tour[i]
        u = tour[i + 1]
        G.add_edge(points[v], points[u], color=tour_color)
    
    # print last edge
    v = tour[0]
    u = tour[-1]
    G.add_edge(points[v], points[u], color=tour_color)
    
    pos = {point: point for point in points}
    labeldict = {}
    i = 0
    for point in points:
        labeldict[point] = str(i)
        i += 1
    
    # add axis
    fig, ax = plt.subplots()
    ax.set_title("total distance {}".format(cost), loc='right')
    colors = nx.get_edge_attributes(G, 'color').values()
    nx.draw(G, pos=pos, node_size=5, ax=ax, with_labels=False, labels=labeldict, edge_color=colors,
            node_color=colors)  # draw nodes and edges
    
    plt.axis("off")
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()


def print_convergence(data, legend):
    size = len(data)
    x = list(range(1, size + 1))
    
    plt.figure(figsize=(6, 4))
    
    plt.plot(x, data, linewidth=2.0, color='green')
    plt.grid(True)
    plt.xlabel('iterations')
    plt.ylabel(legend)
    plt.tight_layout()
    # print(plt.rcParams["figure.figsize"])
    plt.show()
