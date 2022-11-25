import math
import random

import numpy as np


def floyd(graph, vertices):
    # print(vertices)

    # f = np.zeros([vertices + 1, vertices + 1], dtype=int)
    f = np.ones([vertices + 1, vertices + 1], dtype=int) * math.inf
    # print(f)
    for i in range(vertices + 1):
        f[i][i] = 0
    for edge in graph:
        # print(edge)
        f[int(edge[0])][int(edge[1])] = int(edge[2])
        f[int(edge[1])][int(edge[0])] = int(edge[2])
    # print(f)
    for k in range(1, vertices + 1):
        for i in range(1, vertices + 1):
            for j in range(1, vertices + 1):
                if f[i][j] > f[i][k] + f[k][j]:
                    f[i][j] = f[i][k] + f[k][j]
    return f


def print_route(chromosome, edge):
    print("s 0,", end="")
    for i in range(1, len(chromosome) - 1):
        index = chromosome[i]
        if index == -1:
            print("0,0,", end="")
        else:
            e = edge[index]
            print("({0},{1}),".format(e[0], e[1]), end="")
    print("0")


def print_cost(cost):
    print("q {0}".format(cost))


def print_demand(chromosome, demand):
    d = 0
    for i in range(1, len(chromosome)):
        index = chromosome[i]
        if index == -1:
            print(d)
            d = 0
        else:
            d = d + demand[chromosome[i]]


def print_calculate_cost(chromosome, f, depot, cost, demand_edge):
    sum = 0
    end = depot
    for i in chromosome:
        if i == -1:
            sum = sum + f[end][depot]
            end = depot
        else:
            edge = demand_edge[i]
            sum = sum + f[end][edge[0]] + cost[i]
            end = edge[1]
    return int(sum)
    # print("q {0}".format(int(sum)))


def read_file(file):
    f = open(file, encoding='utf-8')

    information = dict()  # information stores the name value pairs in a dictionary
    graph = []  # graph store the start node, end node, cost, demand of edge

    cost = []  # index对应的cost
    demand = []  # index对应的demand
    demand_edge = []

    # read file
    for line in f:
        if line != "END":
            if line.__contains__(":"):
                d = []
                d = line.strip().split(" : ")
                information[d[0]] = d[1]
                # print(information)
            else:
                d = line.strip().split()  # split according to the spaces

                # print(d)
                graph.append(d)
        else:
            break
    f.close()

    for i in range(1, len(graph)):
        edge = graph[i]
        # 将edge进行解构
        v0 = int(edge[0])
        v1 = int(edge[1])
        c = int(edge[2])
        d = int(edge[3])

        cost.append(c)
        demand.append(d)

        demand_edge.append((v0, v1))
    for i in range(len(cost)):
        cost.append(cost[i])
        demand.append(demand[i])
        edge = demand_edge[i]
        demand_edge.append((edge[1], edge[0]))

    return information, graph, cost, demand, demand_edge


# next_edge_index = find_next(free, demand, demand_edge, end, f, residual_capacity, capacity, cost, type)
def find_next(free, demand, demand_edge, end, depot, f, residual_capacity, capacity, cost, type):
    closest_points = []  # 里面存的是索引
    closest_distance = math.inf
    for i in free:
        if demand[i] <= residual_capacity:
            edge = demand_edge[i]
            if f[end][edge[0]] < closest_distance:
                closest_distance = f[end][edge[0]]
                closest_points = [i]
            elif f[end][edge[0]] == closest_distance:
                closest_points.append(i)
    '''
    通过上面的方法，我们已经得到了距离end节点最近的边的集合，现在需要采取不同的策略来在他们之中进行选择
    type与策略的对应关系如下：
    1：随机选择策略
    2：使得任务离始发站最远
    3：使得任务离始发站最近
    4：使得任务需求与花销的比值最大
    5：使得任务需求与花销的比值最小
    6：在容量没过一半时用策略1，否则用策略2
    '''
    # choice from closest points
    if len(closest_points) == 0:
        return None
    elif len(closest_points) == 1:
        return closest_points[0]
    elif type == 1:
        return random.choice(closest_points)
    elif type == 2:  # strategy: maximize the distance from the task to the depot
        maximum_points = []
        maximum_distance = 0
        for index in closest_points:
            d = demand_edge[index]
            if f[d[1]][depot] > maximum_distance:
                maximum_distance = f[d[1]][depot]
                maximum_points = [index]
            elif f[d[1]][depot] == maximum_distance:
                maximum_points.append(index)
        # choice from maximum points
        if len(maximum_points) != 0:
            return random.choice(maximum_points)
        return None
    elif type == 3:  # strategy: minimize the distance from the task to the depot
        minimum_points = []
        minimum_distance = math.inf
        for index in closest_points:
            d = demand_edge[index]
            if f[d[1]][depot] < minimum_distance:
                minimum_distance = f[d[1]][depot]
                minimum_points = [index]
            elif f[d[1]][depot] == minimum_distance:
                minimum_points.append(index)
        # choice from maximum points
        if len(minimum_points) != 0:
            return random.choice(minimum_points)
        return None
    elif type == 4:  # strategy: maximize the term dem(t)/sc(t), where dem(t) and sc(t) are demand and serving cost of task t, respectively;
        maximum_points = []
        maximum_distance = 0
        for index in closest_points:

            if demand[index] / cost[index] > maximum_distance:
                maximum_distance = demand[index] / cost[index]
                maximum_points = [index]
            elif demand[index] / cost[index] == maximum_distance:
                maximum_points.append(index)
        # choice from maximum points
        if len(maximum_points) != 0:
            return random.choice(maximum_points)
        return None
    elif type == 5:  # strategy: minimize the term dem(t)/sc(t), where dem(t) and sc(t) are demand and serving cost of task t, respectively;
        minimum_points = []
        minimum_distance = math.inf
        for index in closest_points:

            if demand[index] / cost[index] < minimum_distance:
                minimum_distance = demand[index] / cost[index]
                minimum_points = [index]
            elif demand[index] / cost[index] == minimum_distance:
                minimum_points.append(index)
        # choice from maximum points
        if len(minimum_points) != 0:
            return random.choice(minimum_points)
        return None
    elif type == 6:  # use rule 1) if the vehicle is less than half - full, otherwise use rule 2)
        if residual_capacity < capacity / 2:
            return find_next(free, demand, demand_edge, end, depot, f, residual_capacity, capacity, cost, 2)
        else:
            return find_next(free, demand, demand_edge, end, depot, f, residual_capacity, capacity, cost, 3)


'''
1.vehicles : the number of vehicles
2.depot : the start point of cars
3.capacity : the capacity of each route
4.demand : the map from demand edge to demand
5.cost : the map from edge to cost
6.f : floyd minimum distance from one point to another
7.type : decide which strategy we use in the process of finding next edge
'''


def path_scanning(vehicles, depot, capacity, demand, demand_edge, cost, f, type):
    # chromosome stores the while information about the routes
    chromosome = [-1]

    # free is the copy of demand and will be popped once a demand edge has been chosen
    free = []
    for i in range(len(demand_edge)):
        if demand[i] > 0:
            free.append(i)

    # routes are the original schedule
    routes = []
    for _ in range(vehicles):
        routes.append([])

    for i in range(vehicles):  # 对于每辆车进行路径规划
        end = depot  # 回到初始节点

        residual_capacity = capacity

        if len(free) == 0:  # 如果free空了意味着所以任务都完成了，可以直接返回规划
            break
        next_edge = (0, 0)
        while True:
            if len(free) == 0:
                break
            next_edge_index = find_next(free, demand, demand_edge, end, depot, f, residual_capacity, capacity, cost, type)
            if next_edge_index is None:
                break
            # 将next——edge的index加入染色体

            chromosome.append(next_edge_index)
            next_edge = demand_edge[next_edge_index]
            # 从free里面去除被选出来的边和其逆边
            free.remove(next_edge_index)
            if next_edge_index < len(demand_edge)/2:
                free.remove(next_edge_index + len(demand_edge)/2)
            else:
                free.remove(next_edge_index - len(demand_edge)/2)

            routes[i].append(next_edge)  # 将next edge加入第i条routes
            residual_capacity = residual_capacity - demand[next_edge_index]  # 更新剩余容量

            end = next_edge[1]  # 更新末枝节点

        chromosome.append(-1)

    return routes, chromosome
