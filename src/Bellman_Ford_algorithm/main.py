import numpy as np
import json
import math
import turtle
import os
import glob
from copy import deepcopy
from PIL import Image
TARGET_BOUNDS = (1024, 1024)


class Graph:
    def __init__(self, adjacency_list):
        """
        V = Num of vertices
        E = Num of edges
        Adjacency_List = sorted adj. list [[[end, value]], ...]
        Edges_Dict = [[start, end, value], ...]
        Incidence_Matrix = standard -1, 0, 1 incidence matrix
        Adjacency_Matrix = standard adjacency matrix
        Distance_List = [[distance, predecessor], ...]
        """
        self.V = self.number_of_nodes(matrix_=adjacency_list, if_print=False)
        self.E = self.number_of_edges(matrix_=adjacency_list, if_print=False)
        self.Adjacency_List = adjacency_list
        self.Edges_Dict = self.from_adjacency_list_to_edges_dict(matrix_=adjacency_list)
        self.Incidence_Matrix = self.from_edges_dict_to_incidence_matrix(matrix_=adjacency_list, dict_=self.Edges_Dict)
        self.Adjacency_Matrix = self.from_edges_dict_to_adjacency_matrix(matrix_=adjacency_list, dict_=self.Edges_Dict)
        self.Distance_List = self.BellmanFord()

    @staticmethod
    def number_of_edges(matrix_, if_print):
        edge_counter = 0
        for row in matrix_:
            for item in row:
                edge_counter += 1
        if if_print:
            print("number of edges is: " + str(edge_counter) + "\n")
        return edge_counter

    @staticmethod
    def number_of_nodes(matrix_, if_print):
        if if_print:
            print("\nnumber of nodes: " + str(len(matrix_)))
        return len(matrix_)

    @staticmethod
    def print_adjacency_list(matrix_to_print):
        print("my adjacency_matrix: ")
        for row in matrix_to_print:
            print(row)

    @staticmethod
    def from_adjacency_list_to_edges_dict(matrix_):
        inc_dict = {}
        edge_count = 0
        row_count = 0
        for row in matrix_:
            for item in row:
                inc_dict[edge_count] = [row_count, item[0], item[1]]
                edge_count += 1
            row_count += 1
        return inc_dict

    def from_edges_dict_to_incidence_matrix(self, matrix_, dict_):
        matrix = np.zeros((self.number_of_nodes(matrix_=matrix_, if_print=False),
                           self.number_of_edges(matrix_=matrix_, if_print=False),), dtype=int)
        for i in range(len(dict_)):
            matrix[dict_[i][0]][i] = 1
            matrix[dict_[i][1]][i] = -1
        return matrix

    def from_edges_dict_to_adjacency_matrix(self, matrix_, dict_):
        matrix = np.zeros((self.number_of_nodes(matrix_=matrix_, if_print=False),
                           self.number_of_nodes(matrix_=matrix_, if_print=False),), dtype=int)
        for i in range(len(dict_)):
            matrix[dict_[i][0]][dict_[i][1]] = 1
        return matrix

    @staticmethod
    def convert_to_string():
        my_string_ = "Num of vertices: " + str(g.V) + "\n\n"
        my_string_ += "Num of edges: " + str(g.E) + "\n\n"
        my_string_ += "Adjacency_List = sorted adj. list [[[end, value]], ...]:\n"
        for item in g.Adjacency_List:
            my_string_ += str(item) + "\n"
        my_string_ += "\nEdges_Dict = [[start, end, value], ...]:\n"
        for i in range(len(g.Edges_Dict)):
            my_string_ += str(i) + ": " + str(g.Edges_Dict[i]) + "\n"
        my_string_ += "\nIncidence_Matrix = standard -1, 0, 1 incidence matrix:\n" + str(g.Incidence_Matrix)
        my_string_ += "\n\nAdjacency_Matrix = standard adjacency matrix:\n" + str(g.Adjacency_Matrix)

        my_string_ += "\n\n[##############################]"
        my_string_ += "\n[##]BELLMAN FORD - ALGORITHM[##]"
        my_string_ += "\n[##############################]"

        my_string_ += "\n\nDistance_List:\n"
        for i in range(len(g.Distance_List)):
            my_string_ += "to Vertex: [" + str(i) +\
                          "] predecessor: [" + str(g.Distance_List[i][1]) +\
                          "]; distance: " + str(g.Distance_List[i][0]) + "\n"
        return my_string_

    @staticmethod
    def convert_to_json():
        inc_list = []
        adj_list = []
        row_list = []
        for row in g.Incidence_Matrix:
            for item in row:
                row_list.append(int(item))
            inc_list.append(deepcopy(row_list))
            row_list.clear()
        for row in g.Adjacency_Matrix:
            for item in row:
                row_list.append(int(item))
            adj_list.append(deepcopy(row_list))
            row_list.clear()

        dict_ = {"V": g.V,
                 "E": g.E,
                 "Adjacency_list": g.Adjacency_List,
                 "Edges_Dict": g.Edges_Dict,
                 "Incidence_Matrix": inc_list,
                 "Adjacency_Matrix": adj_list,
                 "Distance_list": g.Distance_List}
        return dict_

    def try_to_show_turtle_graph(self, file_name_):
        matrix_ = deepcopy(self.Adjacency_Matrix)
        radius = 300
        n = len(matrix_)
        a = float(2 * radius * math.sin(math.pi / n))
        locations = {}

        t = turtle.Turtle()
        t.hideturtle()
        t.speed("fastest")
        t.up()
        t.right(90 + 360 / (2 * n))
        t.forward(radius)
        t.left(90 + 360 / (2 * n))

        for i in range(len(matrix_)):
            locations[i] = t.pos()
            t.forward(a)
            t.forward(a / 6)
            t.left(90)
            t.down()
            t.circle(a / 6)
            t.up()
            t.left(90)
            t.forward(a / 6)
            t.left(180)
            t.left(180 - (180 * (n - 2) / n))

        for i in range(len(matrix_)):
            for j in range(len(matrix_)):
                if matrix_[i][j] == 1:
                    t.up()
                    t.setpos(locations[i])
                    t.down()
                    t.color("blue")
                    t.goto((locations[i][0]+locations[j][0])/2, (locations[i][1]+locations[j][1])/2)
                    t.color("black")
                    for k in range(len(self.Edges_Dict)):
                        if self.Edges_Dict[k][0] == i and self.Edges_Dict[k][1] == j:
                            t.write(self.Edges_Dict[k][2], font=("Arial", 15, "normal"))
                    t.color("red")
                    t.goto(locations[j])
                    matrix_[i][j] = 0
                    matrix_[j][i] = 0

        t.color("black")
        t.up()
        t.speed("fastest")
        for i in range(len(matrix_)):
            t.up()
            if locations[i][1] <= 0:
                t.setpos(locations[i][0] - 3, locations[i][1] - 50)
            else:
                t.setpos(locations[i][0] - 3, locations[i][1] + 33)
            t.down()
            t.write(i, font=("Arial", 15, "normal"))
            t.up()

        t.goto(-410, 375)
        t.down()
        t.color("black")
        t.write("Blue = Start   Red = End   (weight in the middle of the edge) ", font=("Arial", 15, "normal"))
        t.up()
        t.goto(-410, -375)
        t.down()
        t.write("Graph: ", font=("Arial", 15, "normal"))
        t.up()

        cv = turtle.getcanvas()
        cv.postscript(file="file_name.eps", colormode='color')
        # turtle.done()

        pic = Image.open('file_name.eps')
        pic.load(scale=10)
        # Ensure scaling can anti-alias by converting 1-bit or palette images
        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")
        # Calculate the new size, preserving the aspect ratio
        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
        new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
        # Resize to fit the target size
        pic = pic.resize(new_size, Image.ANTIALIAS)
        # Save to PNG
        pic.save("output_graph_" + file_name_ + ".png")

        os.remove("file_name.eps")

    def try_to_show_turtle_path(self, file_name_):
        turtle.clearscreen()
        matrix_ = deepcopy(self.Adjacency_Matrix)
        radius = 300
        n = len(matrix_)
        a = float(2 * radius * math.sin(math.pi / n))
        locations = {}

        t_1 = turtle.Turtle()
        t_1.hideturtle()
        t_1.speed("fastest")
        t_1.up()
        t_1.right(90 + 360 / (2 * n))
        t_1.forward(radius)
        t_1.left(90 + 360 / (2 * n))

        for i in range(len(matrix_)):
            locations[i] = t_1.pos()
            t_1.forward(a)
            t_1.forward(a / 6)
            t_1.left(90)
            t_1.down()
            t_1.circle(a / 6)
            t_1.up()
            t_1.left(90)
            t_1.forward(a / 6)
            t_1.left(180)
            t_1.left(180 - (180 * (n - 2) / n))

        for i in range(len(matrix_)):
            for j in range(len(matrix_)):
                if matrix_[i][j] == 1 and g.Distance_List[j][1] == i:
                    t_1.up()
                    t_1.setpos(locations[i])
                    t_1.down()
                    t_1.color("blue")
                    t_1.goto((locations[i][0] + locations[j][0]) / 2, (locations[i][1] + locations[j][1]) / 2)
                    t_1.color("black")
                    for k in range(len(self.Edges_Dict)):
                        if self.Edges_Dict[k][0] == i and self.Edges_Dict[k][1] == j:
                            t_1.write(self.Edges_Dict[k][2], font=("Arial", 15, "normal"))
                    t_1.color("red")
                    t_1.goto(locations[j])
                    matrix_[i][j] = 0
                    matrix_[j][i] = 0

        t_1.color("black")
        t_1.up()
        t_1.speed("fastest")
        for i in range(len(matrix_)):
            t_1.up()
            if locations[i][1] <= 0:
                t_1.setpos(locations[i][0] - 40, locations[i][1] - 50)
            else:
                t_1.setpos(locations[i][0] - 40, locations[i][1] + 33)
            t_1.down()
            t_1.write(str(i) + "-distance: " + str(g.Distance_List[i][0]), font=("Arial", 15, "normal"))
            t_1.up()

        t_1.goto(-410, 375)
        t_1.down()
        t_1.color("black")
        t_1.write("Blue = Start   Red = End   (weight in the middle of the edge) ", font=("Arial", 15, "normal"))
        t_1.up()
        t_1.goto(-410, -375)
        t_1.down()
        t_1.write("Paths in graph: ", font=("Arial", 15, "normal"))
        t_1.up()

        cv = turtle.getcanvas()
        cv.postscript(file="file_name.eps", colormode='color')
        # turtle.done()

        pic = Image.open('file_name.eps')
        pic.load(scale=10)
        # Ensure scaling can anti-alias by converting 1-bit or palette images
        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")
        # Calculate the new size, preserving the aspect ratio
        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
        new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
        # Resize to fit the target size
        pic = pic.resize(new_size, Image.ANTIALIAS)
        # Save to PNG
        pic.save("output_graph_path_" + file_name_ + ".png")

        os.remove("file_name.eps")

    def BellmanFord(self):
        # distance list init
        dist = [float("Inf")] * self.V
        dist[self.Edges_Dict[0][0]] = 0
        pred = [-1] * self.V

        # relaxing
        for i in range(self.V - 1):
            # dist update
            for j in range(len(self.Edges_Dict)):
                if dist[self.Edges_Dict[j][0]] != float("Inf") and dist[self.Edges_Dict[j][0]] + self.Edges_Dict[j][2] < dist[self.Edges_Dict[j][1]]:
                    dist[self.Edges_Dict[j][1]] = dist[self.Edges_Dict[j][0]] + self.Edges_Dict[j][2]
                    pred[self.Edges_Dict[j][1]] = self.Edges_Dict[j][0]

        # negative check
        for i in range(self.V - 1):
            for j in range(len(self.Edges_Dict)):
                if self.Edges_Dict[j][0] == i:
                    if dist[i] + self.Edges_Dict[j][2] < dist[self.Edges_Dict[j][1]]:
                        fail = [["negative cycle!", "negative cycle!"]] * self.V
                        return fail
        ret = []
        for i in range(len(dist)):
            ret.append([dist[i], pred[i]])
        return ret


if __name__ == '__main__':

    print("[+]Starting...[+]")
    files = glob.glob('output*')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    print("Type file name without .json extension:\n-->", end="")
    file_name = input()
    with open(file_name + ".json") as f:
        my_data = json.load(f)

    g = Graph(adjacency_list=my_data)
    my_string = g.convert_to_string()
    to_json = g.convert_to_json()

    text_file = open("output_info_" + file_name + ".txt", "w")
    text_file.write(my_string)
    text_file.close()
    with open("output_info_" + file_name + ".json", "w") as f:
        json.dump(to_json, f)
    g.try_to_show_turtle_graph(file_name_=file_name)
    if g.Distance_List[0][0] != "negative cycle!":
        g.try_to_show_turtle_path(file_name_=file_name)
    print("[+]Done![+]")
