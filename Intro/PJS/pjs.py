import math
import operator


class Node:
    def __init__(self, ID, x, y, demand):
        self.ID = ID
        self.x = x
        self.y = y
        self.demand = demand
        self.in_route = None
        self.interior = False
        self.dn_edge = None
        self.nd_edge = None
        self.start_linked = False
        self.finish_linked = False


class Edge:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end
        self.cost = 0.0
        self.savings = 0.0
        self.inverted_edge = None
        self.efficiency = 0.0


class Route:
    def __init__(self):
        self.cost = 0.0
        self.edges = []
        self.demand = 0.0
    
    def reverse(self):
        size = len(self.edges)
        for i in range(size):
            edge = self.edges[i]
            inverted_edge = edge.inverted_edge
            self.edges.remove(edge)
            self.edges.insert(0, inverted_edge)

class Solution:
    last_ID = -1

    def __init__(self):
        Solution.last_ID += 1
        self.ID = Solution.last_ID
        self.routes = []
        self.cost = 0.0
        self.demand = 0.0


def read_nodes(filename):
    nodes = []
    with open(filename) as instance:
        i = -3
        for line in instance:
            if i == -3:
                pass
            else:
                data = line.split(";")[1]
                if i == -2:
                    fleet_size = int(data)
                elif i == -1:
                    route_max_cost = float(data)
                else:
                    node_data = [float(x) for x in line.split(";")]
                    nodes.append(Node(i, node_data[0], node_data[1], node_data[2]))
            i += 1
    return nodes, route_max_cost, fleet_size


def pjs(alpha, nodes, max_cost, fleet_size):    
    def is_mergeable(i_node, j_node, i_route, j_route, ij_edge):
        return (
            i_route != j_route and
            i_node.finish_linked and j_node.start_linked and
            max_cost > i_route.cost + j_route.cost - ij_edge.savings
        )

    
    start_node, finish_node = nodes[0], nodes[-1]

    for node in nodes[1:-1]:
        sn_edge = Edge(start_node, node)
        nf_edge = Edge(node, finish_node)
        sn_edge.cost = math.sqrt((node.x - start_node.x)**2 + (node.y - start_node.y)**2)
        nf_edge.cost = math.sqrt((node.x - finish_node.x)**2 + (node.y - finish_node.y)**2)
        node.dn_edge = sn_edge
        node.nd_edge = nf_edge

    eff_list = []
    for i in range(1, len(nodes) - 2):
        i_node = nodes[i]
        for j in range(i+1, len(nodes) - 1):
            j_node = nodes[j]
            ij_edge = Edge(i_node, j_node)
            ji_edge = Edge(j_node, i_node)
            ij_edge.inverted_edge = ji_edge
            ji_edge.inverted_edge = ij_edge
            ij_edge.cost = math.sqrt((j_node.x - i_node.x)**2) + (j_node.y - i_node.y)**2
            ij_savings = i_node.nd_edge.cost + j_node.dn_edge.cost - ij_edge.cost
            e_reward = i_node.demand + j_node.demand
            ij_edge.savings = ij_savings
            ij_edge.efficiency = alpha * ij_savings + (1-alpha) * e_reward
            ji_savings = j_node.nd_edge.cost + i_node.dn_edge.cost - ji_edge.cost
            ji_edge.savings = ji_savings
            ji_edge.efficiency = alpha * ji_savings + (1-alpha) * e_reward
            eff_list += [ij_edge, ji_edge]

    eff_list.sort(key=operator.attrgetter("efficiency"), reverse=True)

    # construct solution
    solution = Solution()
    for node in nodes[1:-1]:
        sn_edge = node.dn_edge
        nf_edge = node.nd_edge
        snf_route = Route()
        snf_route.edges.append(sn_edge)
        snf_route.demand += node.demand
        snf_route.cost += sn_edge.cost
        snf_route.edges.append(nf_edge)
        snf_route.cost += nf_edge.cost
        node.in_route = snf_route
        node.start_linked = True
        node.finish_linked = True
        solution.routes.append(snf_route)
        solution.cost += snf_route.cost
        solution.demand += snf_route.demand

    while len(eff_list) > 0:
        index = 0
        ij_edge = eff_list.pop(index)
        i_node = ij_edge.origin
        j_node = ij_edge.end
        i_route = i_node.in_route
        j_route = j_node.in_route
        if is_mergeable(i_node, j_node, i_route, j_route, ij_edge):
            ji_edge = ij_edge.inverted_edge
            if ji_edge in eff_list:
                eff_list.remove(ji_edge)
            i_edge = i_route.edges[-1]
            i_route.edges.remove(i_edge)
            i_route.cost -= i_edge.cost
            i_node.finish_linked = False
            j_edge = j_route.edges[0]
            j_route.edges.remove(j_edge)
            j_route.cost -= j_edge.cost
            j_node.start_linked = False
            i_route.edges.append(ij_edge)
            i_route.cost += ij_edge.cost
            i_route.demand += j_node.demand
            j_node.in_route = i_route
            for edge in j_route.edges:
                i_route.edges.append(edge)
                i_route.cost += edge.cost
                i_route.demand += edge.end.demand
                edge.end.in_route = i_route
            solution.cost -= ij_edge.savings
            solution.routes.remove(j_route)

    solution.routes.sort(key=operator.attrgetter("demand"), reverse=True)
    for route in solution.routes[fleet_size:]:
        solution.demand -= route.demand
        solution.cost -= route.cost
        solution.routes.remove(route)

    return solution


alphas = [0.3, 0.5, 1.0]
files = ["p5.3.q.txt"]
for greed in alphas:
    for _file in files:
        instance_name = _file.split(".txt")[0]
        nodes, max_cost, fleet_size = read_nodes(_file)
        solution = pjs(greed, nodes, max_cost, fleet_size)
        print(f"Reward obtained with PJS heuristics on {instance_name} is {solution.demand:.2f}")
        print(f"alpha: {greed} || Max cost: {max_cost} || Fleet size: {fleet_size}")
        for route in solution.routes:
            s = str(0)
            for edge in route.edges:
                s = s + '-' + str(edge.end.ID)
            print(f"Route: {s} || Reward = {route.demand:.2f} || Cost / Time = {route.cost:.2f}")
