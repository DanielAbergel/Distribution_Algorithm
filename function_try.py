
import networkx as nx
import math as math
import doctest as doctest
import matplotlib.pyplot as plt
import numpy as np
from networkx import info


def has_negative_cyc(digraph):
    """
    Check if the given graph contains a cycle in which the sum of weights is negative.
    :param digraph: a networkx directed graph object.
    :return: True of the graph contains a directed cycle with negative sum of weights; False otherwise.

    >>> G = nx.DiGraph()
    >>> G.add_edge('a', 'b', weight=4)
    >>> G.add_edge('b', 'c', weight=-2)
    >>> G.add_edge('c', 'a', weight=-1)
    >>> has_negative_cyc(G)
    False

    >>> G['c']['a']['weight'] = -3
    >>> has_negative_cyc(G)
    True
    """
    try:
        path= dict(nx.all_pairs_bellman_ford_path_length(digraph))
        #print(path)
        #print("no negative cyc")
        return False

    except nx.exception.NetworkXUnbounded as e:
        #print(e)
        #print("there is negative cyc")
        return True





def has_cyc_less_than_one(digraph):
    """
    Check if the given graph contains a cycle in which the multiplying of weights is less than one.
    :param digraph: a networkx directed graph object.
    :return: True of the graph contains a directed cycle with ess than one multiplying of weights; False otherwise.

    >>> q = nx.DiGraph()
    >>> q.add_edge('a', 'b', weight=0.1)
    >>> q.add_edge('b', 'c', weight=0.1)
    >>> q.add_edge('c', 'a', weight=0.1)
    >>> has_cyc_less_than_one(q)
    True

       >>> q['c']['a']['weight'] = 1
    >>> has_negative_cyc(q)
    False
    >>> q['c']['a']['weight'] = 10
    >>> has_cyc_less_than_one(q)
    True

    >>> q['c']['a']['weight'] = 1000
    >>> has_cyc_less_than_one(q)
    False
    """
    g = nx.DiGraph()
    for (u, v, d) in digraph.edges(data=True):
       #print(d)
       #g.add_edge(u, v, weight=d['weight'])
       g.add_edge(u,v,weight=(math.log(d['weight'],2)))
    return has_negative_cyc(g)
    #for (u, v, d) in g.edges(data=True):
     #  print(d)
    #return g


def num_of_shared_objects(z):
    """
    return the number of object that shared = belong to more then on agent
    :param z :  matrix  that represent - given allocation
    :return:  number of shared objects

    >>> z = [ [1, 0, 0],[0.8, 0.1, 0.1],[0, 1, 0]]
    >>> num_of_shared_objects(z)
    1
    >>> z1 = [[1, 0, 0],[0.8, 0.1, 0.1],[0.2, 0.6, 0.2]]
    >>> num_of_shared_objects(z1)
    2
    """
    count = 0
    for i in range(0, len(z)):
        for j in range(0, len(z[0])):
            if(z[i][j] == 1):
                break
            if (z[i][j] > 0):
                count += 1
                break
    return count


def num_of_sharing(mat):
    """
    return the number of sharing in given allocation
    :param mat matrix that represent - given allocation
    :return:  number of sharing

    >>> z = [ [1, 0, 0],[0.8, 0.1, 0.1],[0, 1, 0]]
    >>> num_of_sharing(z)
    2
    >>> z1 = [[1, 0, 0],[0.8, 0.1, 0.1],[0.2, 0.6, 0.2]]
    >>> num_of_sharing(z1)
    4
    """
    count = 0
    temp = 0
    for i in range(0, len(mat)):

        for j in range(0, len(mat[0])):
            if(mat[i][j] > 0)and(mat[i][j] < 1):
                temp += 1
        if not (temp == 0):
            temp += -1
            count += temp
            temp = 0

    return count
def mat_to_directed_graph(matz , matv):
    """
    convert the z matrix to directed graph
    :param matv:  represent- the Agents value for the objects
    :param matz: represent - given allocation
    :return: directed_graph
    >>> z = [ [1, 0.8, 0],[0, 0.2, 1]]
    >>> v = [ [4, 2.5, 1],[1.25, 2, 5]]
    >>> str(mat_to_directed_graph(z,v).edges().data())
    "[('i0', 'o0', {'weight': 4}), ('i0', 'o1', {'weight': 2.5}), ('o0', 'i1', {'weight': 0.8}), ('o1', 'i0', {'weight': 0.4}), ('o1', 'i1', {'weight': 0.5}), ('o2', 'i0', {'weight': 1.0}), ('i1', 'o1', {'weight': 2}), ('i1', 'o2', {'weight': 5})]"
    >>> z = [ [1, 0.8, 0],[0, 0.2, 1]]
    >>> v = [ [4, 25, 1],[1.25, 2, 5]]
    >>> str(mat_to_directed_graph(z,v).edges().data())
    "[('i0', 'o0', {'weight': 4}), ('i0', 'o1', {'weight': 25}), ('o0', 'i1', {'weight': 0.8}), ('o1', 'i0', {'weight': 0.04}), ('o1', 'i1', {'weight': 0.5}), ('o2', 'i0', {'weight': 1.0}), ('i1', 'o1', {'weight': 2}), ('i1', 'o2', {'weight': 5})]"
    >>> z = [ [1, 0.3],[0, 0.7]]
    >>> v = [ [7, 2],[1, 3]]
    >>> str(mat_to_directed_graph(z,v).edges().data())
    "[('i0', 'o0', {'weight': 7}), ('i0', 'o1', {'weight': 2}), ('o0', 'i1', {'weight': 1.0}), ('o1', 'i0', {'weight': 0.5}), ('o1', 'i1', {'weight': 0.3333333333333333}), ('i1', 'o1', {'weight': 3})]"
   """
    n = len(matz)
    m = len(matz[0])
    g = nx.DiGraph()
    for i in range(0, n):
        for j in range(0, m):
            if(matz[i][j] > 0):
                if(matv[i][j] >= 0):
                    g.add_edge("i"+str(i), "o"+str(j), weight=(matv[i][j]))
                else:
                    g.add_edge("o"+str(j), "i"+str(i), weight=1/(matv[i][j]))
            if(matz[i][j] < 1):
                if(matv[i][j] > 0):
                    g.add_edge("o"+str(j), "i"+str(i), weight=1/(matv[i][j]))
                else:
                    g.add_edge("i"+str(i), "o"+str(j), weight=(matv[i][j]*-1))
    return g


def mat_to_undirected_graph(matz, matv):
    """
    convert the z matrix to directed graph
    :param matv:  represent- the Agents value for the objects
    :param matz: represent - given allocation
    :return: undirected_graph
    >>> z = [ [1, 0.8, 0],[0, 0.2, 1]]
    >>> v = [ [4, 2.5, 1],[1.25, 2, 5]]
    >>> str(mat_to_undirected_graph(z, v).edges())
    "[('i0', 'o0'), ('i0', 'o1'), ('o1', 'i1'), ('i1', 'o2')]"
    >>> a = [ [1, 0, 0],[0, 1, 0],[0, 0, 1]]
    >>> b  = [ [1, 0, 0],[0, 1, 0],[0, 0, 1]]
    >>> str(mat_to_undirected_graph(a, b).edges())
    "[('i0', 'o0'), ('i1', 'o1'), ('i2', 'o2')]"
    >>> c = [ [1, 1, 1],[1, 1, 1],[1, 1, 1]]
    >>> d  = [ [1, 1, 1],[1, 1, 1],[1, 1, 1]]
    >>> str(mat_to_undirected_graph(c, d).edges())
    "[('i0', 'o0'), ('i0', 'o1'), ('i0', 'o2'), ('o0', 'i1'), ('o0', 'i2'), ('o1', 'i1'), ('o1', 'i2'), ('o2', 'i1'), ('o2', 'i2')]"
    """
    n = len(matz)
    m = len(matz[0])
    g = nx.Graph()
    for i in range(0, n):
        for j in range(0, m):
            if(matz[i][j] > 0):
                g.add_edge("i"+str(i), "o"+str(j), weight=0)
    return g




def find_allocation_for_2(matv):
   pass



def find_all_the_non_sherd_alloc(matv):
    """
    convert allocation that is represent by one demention array
    to complete allocation that represent by matrix
    :param arr:  represent- the allocation that is represent by one demention array
    :return: complete allocation that represent by matrix (matv)
    """
    l = build_the_Difference_array(matv)
    tempalloc=[0]*len(matv[0])
    #print("the temp before: {}".format(tempalloc))
    #print("the l before: {}".format(l))
    print(tempalloc)
    for i in range(0,len(matv[0])):
        for j in range(0,i+1):
           tempalloc[l[j][0]] = 1
        print(tempalloc)
        print(array_to_alloc(tempalloc))

def array_to_alloc(arr):
    """
    convert allocation that is represent by one demention array
    to complete allocation that represent by matrix
    :param arr:  represent- the allocation that is represent by one demention array
    :return: complete allocation that represent by matrix (matv)
    >>> a = [1, 0, 0]
    >>> array_to_alloc(a)
    [[1, 0, 0], [0, 1, 1]]
    >>> a = [1, 0, 1 , 0 , 1 , 1 , 1 , 0]
    >>> array_to_alloc(a)
    [[1, 0, 1, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 0, 0, 1]]
    """
    matv=[]
    matv.append(arr)
    arr2=[]
    for i in range(0,len(arr)):
       arr2.append((1-arr[i]))
    matv.append(arr2)
    return matv





def takeSecond(elem):
    return elem[1]




def build_the_Difference_array(matv):
    """
    this function build the array for ratio between i0 to i1
    and sort it
    :param matv:  represent- the Agents value for the objects
    :return: the sorted array

    >>> a = [[20,30,40,10],[10,60,10,20]]
    >>> build_the_Difference_array(a)
    [(1, 0.5), (3, 0.5), (0, 2.0), (2, 4.0)]
    >>> a = [[1,3,9,2,4,6,5],[2,4,4,3,6,2,1]]
    >>> build_the_Difference_array(a)
    [(0, 0.5), (3, 0.6666666666666666), (4, 0.6666666666666666), (1, 0.75), (2, 2.25), (5, 3.0), (6, 5.0)]
    """
    n=len(matv[0])
    l=[]
    for i in range(0,n):
        temp = matv[0][i]/matv[1][i]
        l.append((i,temp))
    l.sort(key=takeSecond)
    #print(l)
    return l








def matrix_transpose(mat):
    """
    this function transpose matrix
    """
    ans = [[row[i] for row in mat]for i in range(len(mat[0]))]
    return ans




def printmat(matrix):
    """
    this function print matrix in her shape
    """
    for row in matrix:
        print(row)

def print_Dgraph(G):
    """
    print the given graph with matplotlib.pyplot
    :param digraph: a networkx directed graph object.
    :return: none

    """
    # the printing of the graph
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 100]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 100]
    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # Weight
    new_labels = dict(
        map(lambda x: ((x[0], x[1]), str(x[2]['weight'] if x[2]['weight'] <= 3 else "")), G.edges(data=True)))
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=new_labels)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show()






def is_proportional(matz , matv):
    """
    this function check if allocation z is proportional
    according to any agent
    for any i and j: ui(xi)>=1/n(ui(xj)
    :param matz represent the allocation
    :param matv represent the value for the agents
    :return: bool value if the allocation is proportional
    >>> v = [[1,3,5,2],[4,3,2,4]]
    >>> z = [[0,0,1,0.5],[1,1,0,0.5]]
    >>> is_proportional(z,v)
    True
    >>> v = [[11,3],[7,7]]
    >>> z = [[0.5,0.2],[0.5,0.8]]
    >>> is_proportional(z,v)
    False
    >>> v = [[11,3],[7,7]]
    >>> z = [[0.6,0.2],[0.4,0.8]]
    >>> is_proportional(z,v)
    True
    """
    flag = True
    for i in range(0,len(matz)):
        if not(one_proportional(matz , matv,i)):
            flag = False
    return flag


def one_proportional(matz , matv,x):
    """
    this function check if allocation z is proportional
    according to single agent
    for specific i and any j : ui(xi)>=1/n(ui(xj)
    :param matz represent the allocation
    :param matv represent the value for the agents
    :param x the number of agent we check
    :return: bool value if the allocation is proportional
    >>> v = [[1,3,5,2],[4,3,2,4]]
    >>> z = [[0,0,1,0.5],[1,1,0,0.5]]
    >>> one_proportional(z,v,0)
    True
    >>> v = [[1,3,5,2],[4,3,2,4]]
    >>> z = [[0,0,1,0],[1,1,0,1]]
    >>> one_proportional(z,v,0)
    False
    >>> v = [[11,3],[7,7]]
    >>> z = [[0.5,0.2],[0.5,0.8]]
    >>> one_proportional(z,v,0)
    False
    >>> v = [[11,3],[7,7]]
    >>> z = [[0.5,0.2],[0.5,0.8]]
    >>> one_proportional(z,v,1)
    True
    """
    sum = 0
    part = 0
    for i in range(0,len(matz[0])):
        sum += matv[x][i]
        part += matv[x][i]*matz[x][i]
    sum = sum / len(matz)
    return part>=sum




# need to do
def is_envy_free(matz , matv):
    pass



if __name__ == '__main__':
    #v = [[5, 1], [25, 2], [1, 5]]
    #z = [[1, 0], [0.8, 0.2], [0, 1]]
    #G = mat_to_directed_graph(z, v)
    # print_graph(G)
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    #z = [ [1, 0.8, 0],[0, 0.2, 1]]
    #v = [ [4, 25, 1],[1.25, 2, 5]]
     #z = [ [1, 0.3],  [0, 0.7]]
     #v = [ [7, 2], [1,3]]
    #a = [ [1, 0, 0],[0, 1, 0],[0, 0, 1]]
    #b  = [ [1, 0, 0],[0, 1, 0],[0, 0, 1]]
    #c = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    #d = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    #print_Dgraph(mat_to_directed_graph(z,v))
    # print((mat_to_directed_graph(z,v).edges().data()))
    #a=[[1,3,9,2,4,6,5],[2,4,4,3,6,2,1]]
    #find_all_the_non_sherd_alloc(a)



