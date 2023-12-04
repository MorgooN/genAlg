import random
import Chromosome as ch


# cоздаём случайную хромосому (решение) --> случайным образом тасуем лист
def create_random_list(n_list):
    start = n_list[0]  # начальная и конечная позиция должны быть одинаковыми

    temp = n_list[1:] # все элементы листа кроме первого тасуются 
    temp = random.sample(temp, len(temp))  # перетасовка 

    temp.insert(0, start)  # добавляем стартовую точку в начало хромосомы
    temp.append(start)  # добавляем стартовую точку в конец. Маршрут должен заканчивать там же, где и начинался
    return temp

def initialization(data, pop_size):
    initial_population = []
    for i in range(0, pop_size):  # количество хромосом = population_size
        temp = create_random_list(data)
        new_ch = ch.Chromosome(temp)
        initial_population.append(new_ch) # Добавляем новосозданные хромосомы к изначальной популяции
    return initial_population

# выбор родительской хромосомы для создания дочерней
def selection(population):  # турнир
    ticket_1, ticket_2, ticket_3, ticket_4 = random.sample(range(0, 99), 4)  # 4 случайных тикета

    # выбираем случайных образом 4 хромосомы исходя из случайно сгенерированных тикетов
    candidate_1 = population[ticket_1]
    candidate_2 = population[ticket_2]
    candidate_3 = population[ticket_3]
    candidate_4 = population[ticket_4]

    # определяем победителя
    if candidate_1.fitness_value > candidate_2.fitness_value:
        winner = candidate_1
    else:
        winner = candidate_2

    if candidate_3.fitness_value > winner.fitness_value:
        winner = candidate_3

    if candidate_4.fitness_value > winner.fitness_value:
        winner = candidate_4

    return winner  # возвращаем победителя

def crossover(p_1, p_2):
    one_point = random.randint(2, 14)

    child_1 = p_1.chromosome[1:one_point]
    child_2 = p_2.chromosome[1:one_point]

    child_1_remain = [item for item in p_2.chromosome[1:-1] if item not in child_1]
    child_2_remain = [item for item in p_1.chromosome[1:-1] if item not in child_2]

    child_1 += child_1_remain
    child_2 += child_2_remain

    child_1.insert(0, p_1.chromosome[0])
    child_1.append(p_1.chromosome[0])

    child_2.insert(0, p_2.chromosome[0])
    child_2.append(p_2.chromosome[0])

    return child_1, child_2


def crossover_two(p_1, p_2):  # two points crossover
    point_1, point_2 = random.sample(range(1, len(p_1.chromosome)-1), 2)
    begin = min(point_1, point_2)
    end = max(point_1, point_2)

    child_1 = p_1.chromosome[begin:end+1]
    child_2 = p_2.chromosome[begin:end+1]

    child_1_remain = [item for item in p_2.chromosome[1:-1] if item not in child_1]
    child_2_remain = [item for item in p_1.chromosome[1:-1] if item not in child_2]

    child_1 += child_1_remain
    child_2 += child_2_remain

    child_1.insert(0, p_1.chromosome[0])
    child_1.append(p_1.chromosome[0])

    child_2.insert(0, p_2.chromosome[0])
    child_2.append(p_2.chromosome[0])

    return child_1, child_2


def crossover_mix(p_1, p_2):
    point_1, point_2 = random.sample(range(1, len(p_1.chromosome)-1), 2)
    begin = min(point_1, point_2)
    end = max(point_1, point_2)

    child_1_1 = p_1.chromosome[:begin]
    child_1_2 = p_1.chromosome[end:]
    child_1 = child_1_1 + child_1_2
    child_2 = p_2.chromosome[begin:end+1]

    child_1_remain = [item for item in p_2.chromosome[1:-1] if item not in child_1]
    child_2_remain = [item for item in p_1.chromosome[1:-1] if item not in child_2]

    child_1 = child_1_1 + child_1_remain + child_1_2
    child_2 += child_2_remain

    child_2.insert(0, p_2.chromosome[0])
    child_2.append(p_2.chromosome[0])

    return child_1, child_2

# мутация
def mutation(chromosome):  
    mutation_index_1, mutation_index_2 = random.sample(range(1, 19), 2) # генерируем два случайных индекса 
    chromosome[mutation_index_1], chromosome[mutation_index_2] = chromosome[mutation_index_2], chromosome[mutation_index_1] # меняем местами хромосомы исходя из индексов
    return chromosome

# проверяем все хромосомы в поколении и возвращаем лучшую (исходя из стоимости (дистанции))
def find_best(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if generation[n].cost < best.cost:
            best = generation[n]
    return best

# cоздаём новое поколениина основе предыдущих
def create_new_generation(previous_generation, mutation_rate):
    new_generation = [find_best(previous_generation)]  # Элитический метод.Сохраняем лучших из предыдущего поколения. 

    # Создаём две хромосомы. So, iteration size will be half of the population size!
    for a in range(0, int(len(previous_generation)/2)):
        parent_1 = selection(previous_generation) 
        parent_2 = selection(previous_generation)

        child_1, child_2 = crossover_mix(parent_1, parent_2)  # This will create node lists, we need Chromosome objects
        child_1 = ch.Chromosome(child_1)
        child_2 = ch.Chromosome(child_2)

        if random.random() < mutation_rate:
            mutated = mutation(child_1.chromosome)
            child_1 = ch.Chromosome(mutated)

        new_generation.append(child_1)
        new_generation.append(child_2)

    return new_generation

