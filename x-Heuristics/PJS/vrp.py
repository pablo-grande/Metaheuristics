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
        for i, line in enumerate(instance):
            node_data = [float(x) for x in line.split()]
            nodes.append(Node(i, node_data[0], node_data[1], node_data[2]))
    return nodes


def get_depot_edge(a_route, a_node, depot):
    origin = a_route.edges[0].origin
    end = a_route.edges[0].end
    if ((origin == a_node and end == depot) or
        (origin == depot and end == a_node)):
        return a_route.edges[0]
    else:
        return a_route.edges[-1]


def vrp(alpha, nodes, veh_cap):    
    def is_mergeable(i_node, j_node, i_route, j_route, ij_edge):
        if i_route == j_route: return False
        if i_node.interior or j_node.interior: return False
        if veh_cap < i_route.demand + j_route.demand: return False
        return True

    
    depot = nodes[0]

    for node in nodes[1:]:
        dn_edge = Edge(depot, node)
        nd_edge = Edge(node, depot)
        dn_edge.inverted_edge = nd_edge
        nd_edge.inverted_edge = dn_edge
        dn_edge.cost = math.sqrt((node.x - depot.x)**2 + (node.y - depot.y)**2)
        nd_edge.cost = dn_edge.cost
        node.dn_edge = dn_edge
        node.nd_edge = nd_edge

    savings = []
    for i in range(1, len(nodes) - 1):
        i_node = nodes[i]
        for j in range(i+1, len(nodes)):
            j_node = nodes[j]
            ij_edge = Edge(i_node, j_node)
            ji_edge = Edge(j_node, i_node)
            ij_edge.inverted_edge = ji_edge
            ji_edge.inverted_edge = ij_edge
            ij_edge.cost = math.sqrt((j_node.x - i_node.x)**2) + (j_node.y - i_node.y)**2
            ji_edge.cost = ij_edge.cost
            ij_edge.savings = i_node.nd_edge.cost + j_node.dn_edge.cost - ij_edge.cost
            ji_edge.savings = ij_edge.savings
            savings += [ij_edge]

    savings.sort(key=operator.attrgetter("savings"), reverse=True)

    # construct solution
    solution = Solution()
    for node in nodes[1:-1]:
        dn_edge = node.dn_edge
        nd_edge = node.nd_edge
        dnd_route = Route()
        dnd_route.edges.append(dn_edge)
        dnd_route.demand += node.demand
        dnd_route.cost += dn_edge.cost
        dnd_route.edges.append(nd_edge)
        dnd_route.cost += nd_edge.cost
        node.in_route = dnd_route
        node.interior = False
        solution.routes.append(dnd_route)
        solution.cost += dnd_route.cost
        solution.demand += dnd_route.demand

    while len(savings) > 0:
        ij_edge = savings.pop(0)
        i_node = ij_edge.origin
        j_node = ij_edge.end
        i_route = i_node.in_route
        j_route = j_node.in_route
        if is_mergeable(i_node, j_node, i_route, j_route, ij_edge):
            i_edge = get_depot_edge(i_route, i_node, depot)
            i_route.edges.remove(i_edge)
            i_route.cost -= i_edge.cost
            if len(i_route.edges) > 1:
                i_node.interior = True
            if i_route.edges[0].origin != depot:
                i_route.reverse()
            j_edge = get_depot_edge(j_route, j_node, depot)
            j_route.edges.remove(j_edge)
            j_route.cost -= j_edge.cost
            if len(j_route.edges) > 1:
                j_node.interior = True
            if j_route.edges[0].origin != depot:
                j_route.reverse()
            j_route.edges.append(ij_edge)
            i_route.cost += ij_edge.cost
            j_route.demand += j_node.demand
            j_node.in_route = i_route

            for edge in j_route.edges:
                i_route.edges.append(edge)
                i_route.cost += edge.cost
                i_route.demand += edge.end.demand
                edge.end.in_route = i_route
            solution.cost -= ij_edge.savings
            solution.routes.remove(j_route)

    return solution


alphas = [0.3, 0.5, 1.0]
files = ["A-n80-k10_input_nodes.txt"]
veh_cap = 100.0

for alpha in alphas:
    for _file in files:
        instance_name = _file.split(".txt")[0]
        nodes = read_nodes(_file)
        solution = vrp(alpha, nodes, veh_cap)
        print(f"alpha: {alpha} || Veh Cap: {veh_cap}")
        for route in solution.routes:
            s = str(0)
            for edge in route.edges:
                s = s + '-' + str(edge.end.ID)
            print(f"Route: {s} || Cost = {route.demand:.2f}")
