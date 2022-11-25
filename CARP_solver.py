# data = np.fromfile("CARP/CARP_samples/egl-e1-A.dat")
# print(data.shape)
# print(data)
import math
import sys

from util import *

# random.seed(1)
'''
这个版本的解子是用的姚新老师的论文：Memetic Algorithm with Extended Neighborhood Search for Capacitated Arc Routing Problems
'''

if __name__ == "__main__":
    '''
    从命令昂获取运行参数
    '''
    address = sys.argv[1]
    # address = 'CARP_samples/val1A.dat'
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
    required_edges = information['REQUIRED EDGES']
    non_required_edges = information['NON-REQUIRED EDGES']
    vehicles = int(information['VEHICLES'])
    capacity = int(information['CAPACITY'])
    total_cost = information['TOTAL COST OF REQUIRED EDGES']

    '''
    得到图上两点间的最短路径
    '''
    f = floyd(graph[1:], int(vertices))

    routes1, chromosome1 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 1)
    routes2, chromosome2 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 2)
    routes3, chromosome3 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 3)
    routes4, chromosome4 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 4)
    routes5, chromosome5 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 5)
    routes6, chromosome6 = path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, 6)

    # print_route(chromosome1, edge=demand_edge)
    c1 = print_calculate_cost(chromosome1, f, depot, cost, demand_edge)
    # print_cost(c1)

    # print_route(chromosome2, edge=demand_edge)
    c2 = print_calculate_cost(chromosome2, f, depot, cost, demand_edge)
    # print_cost(c2)

    # print_route(chromosome3, edge=demand_edge)
    c3 = print_calculate_cost(chromosome3, f, depot, cost, demand_edge)
    # print_cost(c3)

    # print_route(chromosome4, edge=demand_edge)
    c4 = print_calculate_cost(chromosome4, f, depot, cost, demand_edge)
    # print_cost(c3)

    # print_route(chromosome5, edge=demand_edge)
    c5 = print_calculate_cost(chromosome5, f, depot, cost, demand_edge)
    # print_cost(c5)

    # print_route(chromosome6, edge=demand_edge)
    c6 = print_calculate_cost(chromosome6, f, depot, cost, demand_edge)
    # print_cost(c6)

    # print(chromosome1)

    rank = [(chromosome1, c1), (chromosome2, c2), (chromosome3, c3), (chromosome4, c4), (chromosome5, c5),
            (chromosome6, c6)]
    chro = []
    co = math.inf
    for r in rank:
        if r[1] < co:
            chro = r[0]
            co = r[1]
    print_route(chro, demand_edge)
    print_cost(co)



