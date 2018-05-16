import Graph

class DFS:
    def __init__(self, graph):
        self.__graph = graph
        self.__components = list()
        self.__visited = list()
    
    """
    Deep-First-Search for computing connected components
    """    
    def DFS_components(self):
        vert = self.__graph.get_vertices()
        comp_index = -1
        for i in range(0, len(vert)):
            self.__visited.append(False)
        for i in range(0, len(vert)):
            if(not self.__visited[i]):
                self.__components.append(list())
                comp_index+=1
                self.__components[comp_index].append(vert[i])
                self.t_search_components(i, comp_index)
        rtn = self.__components
        self.__visited = list()
        self.__components = list()
        return rtn
    
    def t_search_components(self, node_idx, comp_idx):
        self.__visited[node_idx] = True
        node_name = self.__graph.get_vertex_name_by_index(node_idx)
        incident_edges = self.__graph.get_incident_edges(node_name)
        for i in range(0, len(incident_edges)):
            adj_vertex_idx = self.__graph.get_vertex_index_by_name(incident_edges[i][1])
            if not self.__visited[adj_vertex_idx]:
                self.__components[comp_idx].append(incident_edges[i][1])
                self.t_search_components(adj_vertex_idx, comp_idx)

