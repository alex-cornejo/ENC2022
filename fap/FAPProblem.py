class FAPEdge(object):
    def __init__(self, i: int, j: int, dij: int, pij: int) -> None:
        self.i = i
        self.j = j
        self.dij = dij
        self.pij = pij


def read_problem(input_file: str):
    n = -1
    E = []
    with open(input_file) as file:
        for line in file:
            line = line.strip()
            line = " ".join(line.split())
            line_arr = line.split(" ")
            i = int(line_arr[0])
            j = int(line_arr[1])
            dij = int(line_arr[4])
            pij = int(line_arr[5])
            E.append(FAPEdge(i, j, dij, pij))
            
            n = max(n, i)
            n = max(n, j)
    # returns |V| and E
    return n + 1, E
