
import copy

class CarData:
    key = 0
    inf = 99999
    def __init__(self,Id,x,y,state):
        self.Id = Id
        self.x = x
        self.y = y
        self.state = state

    def dijkstra(self,mygraph,src,myfocus):
        # 判断图是否为空，如果为空直接退出
        graph = copy.deepcopy(mygraph)
        focus = copy.deepcopy(myfocus)
        if graph is None:
            return None
        nodes = [i for i in range(len(graph))]  # 获取图中所有节点
        visited=[]  # 表示已经路由到最短路径的节点集合
        if src in nodes:
            visited.append(src)
            nodes.remove(src)
        else:
            return None
        distance={src:0}  # 记录源节点到各个节点的距离
        for i in nodes:
            distance[i]=graph[src][i]  # 初始化
        # print(distance)
        path={src:{src:[]}}  # 记录源节点到每个节点的路径
        k=pre=src
        while nodes:
            mid_distance=float('inf')
            for v in visited:
                for d in nodes:
                    new_distance = graph[src][v]+graph[v][d]
                    if new_distance < mid_distance:
                        mid_distance=new_distance
                        graph[src][d]=new_distance  # 进行距离更新
                        k=d
                        pre=v
            distance[k]=mid_distance  # 最短路径
            path[src][k]=[i for i in path[src][pre]]
            path[src][k].append(k)
            # 更新两个节点集合
            visited.append(k)
            nodes.remove(k)
        max_val = self.inf
        for val in focus:
            if(distance[val] < max_val):
                self.key = val
                max_val = distance[self.key]
        return path[src][self.key]

    def load_graph(self,obt):
        mylist = [[self.inf] * 84 for row in range(84)]
        for val in range(84):
            mylist[val][val] = 0
        for line in open('graph.txt'):
            a = int(line.split(' ')[0])
            b = int(line.split(' ')[1])
            if (a != obt and b != obt):
                mylist[a][b] = 1
                mylist[b][a] = 1
        return mylist
    print("CarData init complete")
