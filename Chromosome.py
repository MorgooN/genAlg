import math


class Node:  # Node = Location = Point
    def __init__(self, id, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = int(id)

# получаем набор данных для TSP
file_name = "training_dataset"  
dataset = []

with open(file_name, "r") as f:
    for line in f:  # check each line
        new_line = line.strip()  # удаляем пробелы 
        new_line = new_line.split(" ")  # разбиваем строки
        id, x, y = new_line[0], new_line[1], new_line[2]  
        dataset.append(Node(id=id, x=x, y=y))  # создаём объект Node и добавляем в дата_лист

N = 20 # количество точек (городов)

# в самом начале создаём матрицу расстояний между точками (городами)
def create_distance_matrix(node_list):
    matrix = [[0 for _ in range(N)] for _ in range(N)]

    # classical matrix creation with two for loops
    for i in range(0, len(matrix)-1):
        for j in range(0, len(matrix[0])-1):
            # вычисляем евклидово расстояние между двумя точками и пушим в матрицу
            # a^2 = b^2 + c^2
            matrix[node_list[i].id][node_list[j].id] = math.sqrt(
                pow((node_list[i].x - node_list[j].x), 2) + pow((node_list[i].y - node_list[j].y), 2)
            )
    return matrix

