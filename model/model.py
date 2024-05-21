from datetime import time, datetime

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):

        self._graph = nx.Graph()

    def buildGraph(self, year):
        self._countries = DAO.getAllCountries(year)
        self._idMap = {}
        for c in self._countries:
            self._idMap[c.CCode] = c

        self._graph.clear()
        borders = DAO.getCountryPairs(self._idMap, year)
        self._graph.add_nodes_from(self._countries)
        for b in borders:
            self._graph.add_edge(b.c1, b.c2)

    def getNodes(self):
        return list(self._graph.nodes)

    def getNumConfinanti(self, v):
        return len(list(self._graph.neighbors(v)))

    def getNumCompConnesse(self):
        # S = [self._graph.subgraph(c).copy() for c in nx.connected_components(self._graph)] #this is to get all the components
        return nx.number_connected_components(self._graph)

    def getRaggiungibili(self,n):
        tic = datetime.now()
        a = self.getRaggiungibiliDFS(n)
        print(f"DFS: {datetime.now()-tic} - {len(a)}" )

        tic = datetime.now()
        b = self.getRaggiungibiliBFS(n)
        print(f"BFS: {datetime.now() - tic} - {len(b)}")

        tic = datetime.now()
        c = self.getRaggiungibiliIterative(n)
        print(f"ITER: {datetime.now() - tic} - {len(c)}")

        tic = datetime.now()
        d = self.getRaggiungibiliRecursive(n)
        print(f"REC: {datetime.now() - tic} - {len(d)}")
        return a
    def getRaggiungibiliDFS(self, n):
        tree = nx.dfs_tree(self._graph, n)
        a = list(tree.nodes)
        a.remove(n)
        return a

    def getRaggiungibiliBFS(self, n):
        tree = nx.bfs_tree(self._graph, n)
        a = list(tree.nodes)
        a.remove(n)
        return a

    def getRaggiungibiliIterative(self, n):
        from collections import deque

        # Create two lists: one for visited nodes and one for nodes to be visited
        visited = []
        toBeVisited = deque()

        # Add the starting node to the list of visited vertices
        visited.append(n)

        # Add all neighbors of the starting node to the nodes to be visited
        toBeVisited.extend(self._graph.neighbors(n))

        while toBeVisited:
            # pick the vertex at the front of the queue
            temp = toBeVisited.popleft()

            # Add the node to the list of visited nodes
            visited.append(temp)

            # Get all neighbors of the node
            neighbors = list(self._graph.neighbors(temp))

            # Remove from this list the elements that are already in "visited"
            neighbors = [neighbor for neighbor in neighbors if neighbor not in visited]

            # Remove from this list the elements that are already in "toBeVisited"
            neighbors = [neighbor for neighbor in neighbors if neighbor not in toBeVisited]

            # Add the remaining to the queue of those to be visited
            toBeVisited.extend(neighbors)

        # Return the list of all reachable nodes
        visited.remove(n)
        return visited

    def getRaggiungibiliRecursive(self, n):
        visited = []
        self._recursive_visit(n, visited)
        visited.remove(n)
        return visited

    def _recursive_visit(self, n, visited):
        visited.append(n)

        # Iterate through all neighbors of n
        for c in self._graph.neighbors(n):
            # Filter: visit c only if it hasn't been visited yet
            if c not in visited:
                self._recursive_visit(c, visited)
