import matplotlib.pyplot as plt


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
