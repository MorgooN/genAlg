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
    matrix = [[0 for _ in range(N)] for _ in range(N)] # NxN matrix

    # classical matrix creation with two for loops
    for i in range(0, len(matrix)-1):
        for j in range(0, len(matrix[0])-1):
            # вычисляем евклидово расстояние между двумя точками и пушим в матрицу
            # a^2 = b^2 + c^2
            matrix[node_list[i].id][node_list[j].id] = math.sqrt(
                pow((node_list[i].x - node_list[j].x), 2) + pow((node_list[i].y - node_list[j].y), 2)
            )
    return matrix

matrix = create_distance_matrix(dataset) #Создаём матрицу. Вычисляем расстояние между всеми точками датасета 

# Chromosome = Solution = Path
# Хромосомы будут состоять из Node объектов. Используется во всех стадиях алгоритма.
# Chromosome cost will be used to compare the chromosomes
# We want to minimize the cost. So, lower cost is better!
class Chromosome:
    def __init__(self, node_list):
        self.chromosome = node_list # хромосома = нод_лист

        chr_representation = []
        for i in range(0, len(node_list)):
            chr_representation.append(self.chromosome[i].id)
        self.chr_representation = chr_representation

        distance = 0
        for j in range(1, len(self.chr_representation) - 1):  # get distances from the matrix
            distance += matrix[self.chr_representation[j]-1][self.chr_representation[j + 1]-1]
        self.cost = distance # расстояние в каждой хромосоме = цена рассматриваемой хромосомы

        self.fitness_value = 1 / self.cost

