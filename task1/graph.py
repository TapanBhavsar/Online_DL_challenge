from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, parent, child):
        if child not in self.graph[parent]:
            self.graph[parent].append(child)

    def find_all_siblings(self, node):
        visited = {}
        initial_state =list(self.graph.keys())[0]
        
        queue = []
        siblings = []
        
        queue.append(initial_state)
        visited[initial_state] = True

        while queue:
            initial_state = queue.pop(0)
            for i in self.graph[initial_state]:
                if visited.get(i) == None:
                    if i == node:
                        siblings += self.graph[initial_state]
                    queue.append(i)
                    visited[i] = True
        
        return siblings

    def find_path(self, initial_state, node, discovered, path):
        discovered[initial_state] = True    
        path.append(initial_state)

        if initial_state == node:
            return True

        for i in self.graph[initial_state]:
            if discovered.get(i) == None:
                if self.find_path(i, node, discovered, path):
                    return True

        path.pop()
        return False

    def find_ancesters(self, node):
        initial_state = list(self.graph.keys())[0]
        discovered = {}
        path = []
        path_availability = self.find_path(initial_state, node, discovered, path)
        if path_availability:
            return path
        else:
            return []
