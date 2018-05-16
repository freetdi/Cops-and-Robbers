import DFS
import copy

class Graph(object):
    #type of graph: adjacency list
    def __init__(self, graph=list(), name = "G"):
        self.__graph = graph
        self.__graph_copy = copy.deepcopy(graph)
        
        self.__name = name
        
        #for faster access
        self.__vertices = self.get_vertices()
        self.__edges = self.get_edges(only_once=False)
        
        self.__GRAPH_DEBUG = list()

    def isEmpty(self):
        return len(self.__graph) == 0
        
    def getElem(self, idx1, idx2):
        return self.__graph[idx1][idx2]
    
    def get_vertices_count(self):
        return len(self.__graph)
    
    def get_edges_count(self):
        cnt = 0
        for i in range(0, len(self.__graph)):
            cnt += len(self.__graph[i])-1
        return cnt/2
        
    def exists_vertex(self, v):
        return (v in self.__vertices)

    def exists_edge(self, v1, v2):
        if not self.exists_vertex(v1):
            self.__GRAPH_DEBUG.append("[Graph.exists_edge]: vertex [" + str(v1) + "]")
            return False
        if not self.exists_vertex(v2):
            self.__GRAPH_DEBUG.append("[Graph.exists_edge]: vertex [" + str(v2) + "]")
            return False
            
        v1_idx = self.get_vertex_index_by_name(v1)
        for i in range(0, len(self.__graph[v1_idx])):
            if self.__graph[v1_idx][i] == v2:
                return True
        
    def get_vertices(self):
        tmp = list()
        for i in range(0, len(self.__graph)):
            tmp.append(self.__graph[i][0])
        return tmp
    
    def get_edges(self, only_once=False):
        tmp = list()
        for i in range(0, len(self.__graph)):
            v1 = self.__graph[i][0]
            for j in range(1, len(self.__graph[i])):
                v2 = self.__graph[i][j]
                if [v1, v2] in tmp or [v2, v1] in tmp:
                    continue
                tmp.append([v1, v2])
        return tmp
       
    def get_vertex_index_by_name(self, vertex):
        for i in range(0, len(self.__vertices)):
            if (self.__vertices[i] == vertex):
                return i
        self.__GRAPH_DEBUG.append("[Graph.get_vertex_index_by_name]: vertex [" + str(vertex) + "] does not exist")
        return -1
    
    def get_vertex_name_by_index(self, index):
        if len(self.__vertices) <= index:
            self.__GRAPH_DEBUG.append("[Graph.get_vertex_name_by_index]: index out of range")
            return ""
        return self.__vertices[index]

    def add_vertex(self, vertex):
        if self.exists_vertex(vertex):
            self.__GRAPH_DEBUG.append("[Graph.add_vertex]: vertex [" + str(vertex) + "] still exists")
            return False
        self.__graph.append(list())
        self.__graph[len(self.__graph)-1].append(vertex)
        self.__vertices.append(vertex)
        return True
        
    def remove_vertex(self, vertex):
        if not self.exists_vertex(vertex):
            self.__GRAPH_DEBUG.append("[Graph.remove_vertex]: vertex [" + str(vertex) + "] does not exist")
            return False
            
        for i in range(0, len(self.__graph)):
            if self.__graph[i][0] == vertex:
                self.__graph.pop(i)
                self.__vertices.pop(i)
                break

        for i in range(0, len(self.__graph)):
            for j in range(1, len(self.__graph[i])):
                if self.__graph[i][j] == vertex:
                    self.__graph[i].pop(j)
                    break
                
        return True
    
    def delete_vertices(self, to_delete):
        for i in to_delete:
            self.remove_vertex(i)

    def delete_edges(self, to_delete):
        for i in range(0, len(to_delete)):
            self.remove_edge(to_delete[i][0], to_delete[i][1])
            
    def add_edge(self, v1, v2):
        if v1 not in self.__vertices:
            self.__GRAPH_DEBUG.append("[Graph.add_edge]: cannot create edge: vertex [" + str(v1) + "] does not exist")
            return False
        elif v2 not in self.__vertices:
            self.__GRAPH_DEBUG.append("[Graph.add_edge]: cannot create edge: vertex [" + str(v2) + "] does not exist")
            return False
        elif self.exists_edge(v1, v2):
            self.__GRAPH_DEBUG.append("[Graph.add_edge]: edge [" + str(v1) + ", " + str(v2) + "] still exists")
            return False
            
        else:
            for i in range(0, len(self.__graph)):
                if(self.__graph[i][0] == v1):
                    self.__graph[i].append(v2)
                    break
            for i in range(0, len(self.__graph)):
                if(self.__graph[i][0] == v2):
                    self.__graph[i].append(v1)
                    return True
            return True
                
    def remove_edge(self, v1, v2):
        if not self.exists_edge(v1, v2):
            self.__GRAPH_DEBUG.append("[Graph.remove_edge]: edge [" + str(v1) + ", " + str(v2) + "] does not exist")
        for i in range(0, len(self.__graph)):
            if self.__graph[i][0] == v1:
                for j in range(1, len(self.__graph[i])):
                    if self.__graph[i][j] == v2:
                        self.__graph[i].pop(j)
                        break
                break
        for i in range(0, len(self.__graph)):
            if self.__graph[i][0] == v2:
                for j in range(1, len(self.__graph[i])):
                    if self.__graph[i][j] == v1:
                        self.__graph[i].pop(j)
                        break
                break
        if [v1, v2] in self.__edges:
            self.__edges.pop(self.__edges.index([v1,v2]))
        return True

    def get_incident_edges(self, vertex):
        tmp = list()
        if (vertex in self.get_vertices()):
            for i in range(0, len(self.__graph)):
                if (self.__graph[i][0] == vertex):
                    for j in range(1, len(self.__graph[i])):
                        tmp.append([self.__graph[i][0], self.__graph[i][j]])
        else:
            self.__GRAPH_DEBUG.append("[Graph.get_incident_edges]: vertex [" + str(vertex) + "] does not exist")
            return []
        return tmp

    def get_components_DFS(self):
        tmp = DFS.DFS(copy.deepcopy(self))
        return tmp.DFS_components()

    def get_graph_as_list(self):
        return self.__graph

    def vertices(self):
        return self.__vertices

    def edges(self):
        return self.get_edges()

    def graphtype(self):
        return "boost_graph_undirected"


