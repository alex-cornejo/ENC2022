import math


class InstanceTSPLIB(object):

    def __init__(self) -> None:
        self.EDGE_WEIGHT_TYPE = None
        self.DIMENSION = None
        self.EDGE_WEIGHT_FORMAT = None
        self.NODE_COORD_TYPE = "NO_COORDS"
        self.DISPLAY_DATA_TYPE = "NO_DISPLAY"
        self.DISPLAY_DATA_SECTION = []
        self.NODE_COORD_SECTION = []
        self.EDGE_WEIGHT_SECTION = []

    def set_DIMENSION(self, n):
        self.DIMENSION = n

    def set_EDGE_WEIGHT_TYPE(self, EDGE_WEIGHT_TYPE):
        self.EDGE_WEIGHT_TYPE = EDGE_WEIGHT_TYPE

    def set_EDGE_WEIGHT_FORMAT(self, EDGE_WEIGHT_FORMAT):
        self.EDGE_WEIGHT_FORMAT = EDGE_WEIGHT_FORMAT

    def set_DISPLAY_DATA_TYPE(self, DISPLAY_DATA_TYPE):
        self.DISPLAY_DATA_TYPE = DISPLAY_DATA_TYPE
        if DISPLAY_DATA_TYPE == "COORD_DISPLAY":
            self.DISPLAY_DATA_SECTION = self.NODE_COORD_SECTION

    def set_NODE_COORD_TYPE(self, NODE_COORD_TYPE):
        self.NODE_COORD_TYPE = NODE_COORD_TYPE

    def add_DISPLAY_DATA(self, data):
        if self.DISPLAY_DATA_TYPE == "COORD_DISPLAY" or self.DISPLAY_DATA_TYPE=="NO_DISPLAY":
            raise Exception("Inconsistent DISPLAY_DATA!!")
        self.DISPLAY_DATA_SECTION.append(data)

    def add_NODE_COORD(self, data):
        self.NODE_COORD_SECTION.append(data)

    def add_EDGE_WEIGHT(self, data):
        self.EDGE_WEIGHT_SECTION.append(data)


def compute_distance_matrix(instance: InstanceTSPLIB):

    n = instance.DIMENSION

    # setup distance matrix
    D = [[0] * n for i in range(0, n)]

    # distance functions
    if instance.EDGE_WEIGHT_TYPE == "EXPLICIT":
        edge_weight_data = instance.EDGE_WEIGHT_SECTION

        if instance.EDGE_WEIGHT_FORMAT == "FULL_MATRIX":
            idx_value = 0
            for i in range(0, n):
                for j in range(0, n):
                    D[i][j] = edge_weight_data[idx_value]
                    idx_value += 1

        elif instance.EDGE_WEIGHT_FORMAT == "UPPER_ROW":
            idx_value = 0
            for i in range(0, n):
                for j in range(i+1, n):
                    D[j][i] = D[i][j] = edge_weight_data[idx_value]
                    idx_value += 1

        elif instance.EDGE_WEIGHT_FORMAT == "UPPER_DIAG_ROW":
            idx_value = 0
            for i in range(0, n):
                for j in range(i, n):
                    D[j][i] = D[i][j] = edge_weight_data[idx_value]
                    idx_value += 1


        elif instance.EDGE_WEIGHT_FORMAT == "LOWER_DIAG_ROW":
            idx_value = 0
            for i in range(0, n):
                for j in range(0, i+1):
                    D[j][i] = D[i][j] = edge_weight_data[idx_value]
                    idx_value += 1
        else:
            raise Exception("Inconsistent EDGE_WEIGHT_FORMAT!")


    # compute distances from NODE_COORD_SECTION
    node_data = instance.NODE_COORD_SECTION
    if instance.EDGE_WEIGHT_TYPE == "EUC_2D":
        for i in range(0, n):
            for j in range(i + 1, n):
                dij = math.sqrt((node_data[i][0] - node_data[j][0])
                                ** 2 + (node_data[i][1] - node_data[j][1]) ** 2)
                D[j][i] = D[i][j] = int(dij + 0.5)

    if instance.EDGE_WEIGHT_TYPE == "CEIL_2D":
        for i in range(0, n):
            for j in range(i + 1, n):
                dij = math.sqrt((node_data[i][0] - node_data[j][0])
                                ** 2 + (node_data[i][1] - node_data[j][1]) ** 2)
                D[j][i] = D[i][j] = math.ceil(dij)

    if instance.EDGE_WEIGHT_TYPE == "ATT":
        for i in range(0, n):
            for j in range(i + 1, n):

                xd = node_data[i][0] - node_data[j][0]
                yd = node_data[i][1] - node_data[j][1]
                rij = math.sqrt((xd*xd + yd*yd) / 10.0)
                tij = int(rij + 0.5)
                if (tij < rij):
                    dij = tij + 1
                else:
                    dij = tij
                D[j][i] = D[i][j] = dij

    if instance.EDGE_WEIGHT_TYPE == "GEO":
        PI = 3.141592
        RRR = 6378.388
        for i in range(0, n):
            for j in range(i + 1, n):

                # compute lat and lng of i
                # deg = int(node_data[i][0] + 0.5)
                deg = int(node_data[i][0])
                min = node_data[i][0] - deg
                latitudei = PI * (deg + 5.0 * min / 3.0) / 180.0
                #deg = int(node_data[i][1] + 0.5)
                deg = int(node_data[i][1])
                min = node_data[i][1] - deg
                longitudei = PI * (deg + 5.0 * min / 3.0) / 180.0

                # compute lat and lng of j
                # deg = int(node_data[j][0] + 0.5)
                deg = int(node_data[j][0])
                min = node_data[j][0] - deg
                latitudej = PI * (deg + 5.0 * min / 3.0) / 180.0
                # deg = int(node_data[j][1] + 0.5)
                deg = int(node_data[j][1])
                min = node_data[j][1] - deg
                longitudej = PI * (deg + 5.0 * min / 3.0) / 180.0

                # compute distance between i and j
                q1 = math.cos(longitudei - longitudej)
                q2 = math.cos(latitudei - latitudej)
                q3 = math.cos(latitudei + latitudej)
                dij = int(RRR * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)

                D[j][i] = D[i][j] = dij

    return D
            
        


"""Returns an nxn distance matrix of integers, the list
of coordinates of the nodes (if possible) for plotting, and the EDGE_WEIGHT_TYPE"""


def read_TSPLIB_instance(input_file):

    I = InstanceTSPLIB()

    n = None
    data_type = None

    file = open(input_file, "r")
    for line in file:
        line = line.strip()
        if line == "EOF":
            break

        if line.startswith("DISPLAY_DATA_SECTION") or line.startswith("EDGE_WEIGHT_SECTION"):
            data_type = line.strip()
            continue
        
        if line.startswith("NODE_COORD_SECTION"):
            data_type = line.strip()
            I.set_NODE_COORD_TYPE("TWOD_COORDS")
            I.set_DISPLAY_DATA_TYPE("COORD_DISPLAY")
            continue

        if data_type is not None:
            arr_line = line.split()
            if data_type == "EDGE_WEIGHT_SECTION" and I.EDGE_WEIGHT_TYPE == "EXPLICIT":
                for value in arr_line:
                    I.add_EDGE_WEIGHT(int(value))
            else:
                del arr_line[0]
                if data_type == "NODE_COORD_SECTION":
                    I.add_NODE_COORD([float(value) for value in arr_line])
                else:
                    I.add_DISPLAY_DATA([float(value) for value in arr_line])

        if line.startswith("DIMENSION"):
            arr_line = line.split(":")
            n = int(arr_line[1])
            I.set_DIMENSION(n)
            continue

        if line.startswith("EDGE_WEIGHT_TYPE"):
            arr_line = line.split(":")
            I.set_EDGE_WEIGHT_TYPE(arr_line[1].strip())
            continue

        if line.startswith("DISPLAY_DATA_TYPE"):
            arr_line = line.split(":")
            I.set_DISPLAY_DATA_TYPE(arr_line[1].strip())
            continue

        if line.startswith("EDGE_WEIGHT_FORMAT"):
            arr_line = line.split(":")
            I.set_EDGE_WEIGHT_FORMAT(arr_line[1].strip())


    D = compute_distance_matrix(I)

    file.close()
    return D, I


# test code
#instanceEUC_2D = "TSPLIB/burma14.tsp"
# instanceEUC_2D = "TSPLIB/fri26.tsp"
# instanceEUC_2D = "TSPLIB/a280.tsp"
# instanceEUC_2D = "TSPLIB/att48.tsp"
# instanceEUC_2D = "TSPLIB/bayg29.tsp"
# instanceEUC_2D = "TSPLIB/dantzig42.tsp"
# instanceEUC_2D = "TSPLIB/hk48.tsp"
# instanceEUC_2D = "TSPLIB/pla33810.tsp"
# instanceEUC_2D = "TSPLIB/pla85900.tsp"

# D, I = read_TSPLIB_instance(instanceEUC_2D)
# print("finished")
