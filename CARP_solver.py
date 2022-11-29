# data = np.fromfile("CARP/CARP_samples/egl-e1-A.dat")
# print(data.shape)
# print(data)
import sys
from util import *

# random.seed(1)
'''
这个版本的解子是用的在pathscanning process randomly choose strategy
'''

if __name__ == "__main__":
    '''
    从命令行获取运行参数
    '''
    address = sys.argv[1]
    # address = 'CARP_samples/egl-e1-A.dat'
    t = sys.argv[3]
    # t = 3
    random.seed(sys.argv[5])
    # random.seed(5)

    '''
    读取文件的内容
    '''
    information, graph, cost, demand, demand_edge = read_file(address)

    '''
    通过information掌握所有给出的信息
    '''
    paths = []
    vertices = information['VERTICES']
    depot = int(information['DEPOT'])
    required_edges = int(information['REQUIRED EDGES'])
    non_required_edges = information['NON-REQUIRED EDGES']
    vehicles = int(information['VEHICLES'])
    capacity = int(information['CAPACITY'])
    total_cost = information['TOTAL COST OF REQUIRED EDGES']

    '''
    得到图上两点间的最短路径
    '''
    f = floyd(graph[1:], int(vertices))


    chromosomes = []
    sequences = []
    for i in range(10000):
        sequence = []
        for j in range(vehicles):
            sequence.append(random.randint(1, 6))
        while sequence in sequence:
            sequence = []
            for j in range(vehicles):
                sequence.append(random.randint(1, 6))
        sequences.append(sequence)
        route_random, chromosome_random = random_path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f,
                                                               sequence)
        c_random = calculate_cost(chromosome_random, f, depot, cost, demand_edge)
        chromosomes.append((chromosome_random, c_random))
        if i % 100:
            chromosomes.sort(key=lambda x: x[1])
            chromosomes = chromosomes[0:100]

    chromosomes.sort(key=lambda x: x[1])

    c = chromosomes[0]
    # print(c)
    print_route(c[0], demand_edge)
    print_cost(c[1])
