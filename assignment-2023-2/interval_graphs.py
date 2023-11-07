import argparse
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument('task', choices=[
                    'lexbfs', 'chordal', 'interval'], nargs=1)
parser.add_argument('input_filename')
obj= parser.parse_args()
file= open(obj.input_filename)
task= obj.task[0]

cl= file.read().split()
cl= [int(x) for x in cl]
clusters= set(cl) 
clusters= list(clusters)

nb = []
for i in clusters:
    row = []
    indexes = [index for index, cell in enumerate(cl) if cell == i]
    for j in clusters:
        if i== j:
            row.append(0)
            continue
        is_nbr = False
        for x in indexes:
            if (x%2== 0 and cl[x+1]== j) or (x%2== 1 and cl[x-1]== j):
                is_nbr = True
                break
        if is_nbr:
            row.append(0)
        else:
            row.append(1)
    nb.append(row)

      
def neighbors(u):
    n= []
    for v in clusters:
        if nb[u][v]== 0 and u!= v:
           n.append(v) 
    return n 


def lexbfs(clusters):
    lexicographic= [clusters[0]]
    nbr= neighbors(clusters[0])
    not_nbr= [x for x in clusters if x not in nbr]
    del not_nbr[0]
    s= [nbr, not_nbr]
    while len(s)> 0:
        u= s[0][0]
        nu= neighbors(u)
        lexicographic.append(u)
        s[0].remove(u)
        if len(s[0])== 0:
            s.remove(s[0])
        if len(s)== 0:
            break
        for i in s[:]:
            n = []
            index = s.index(i)
            for j in i[:]:
                if j in nu:
                    n.append(j)
                    i.remove(j)
            if len(n) > 0:
                s.insert(index, n)
        for x in s[:]:
            if len(x)== 0:
                s.remove(x) 
    return lexicographic
    
    
def chordal(lexicographic):
    RNu= []
    for u in lexicographic:
        Nu= neighbors(u)
        RNu= [x for x in lexicographic if x in Nu and lexicographic.index(u)< lexicographic.index(x)]
        if len(RNu)> 0:   
            v= RNu[0]
            RNu.remove(v)
            Nv= neighbors(v)
            RNv= [x for x in lexicographic if x in Nv and lexicographic.index(v)< lexicographic.index(x)]
            if not (set(RNu) <= set(RNv)):
                return False
    return True

def simple_bfs(nodes):
    node= nodes[0]
    visited= []
    queue = deque()
    visited.append(node)
    queue.appendleft(node)
    while len(queue)!= 0:
        c = queue.popleft() 
        for v in neighbors(c):
            if v not in visited and v in nodes:
                visited.append(v)
                queue.appendleft(v)
    return visited


def connected_component(nodes, v):
    comp= simple_bfs(nodes)
    if v in comp:
        return comp
    elif len(comp)!= len(nodes):
        component_len= len(comp)
        while component_len!= len(nodes):
            c= simple_bfs([x for x in nodes if x not in comp])
            if v in c:
                return c
            component_len+= len(c)
            comp.extend(c)
         
            
def interval():
    C = []
    for u in range(len(clusters)):
        row= []
        for v in range(len(clusters)):
            if nb[u][v]== 1:
                nodes= [x for x in clusters if nb[u][x]== 1]
                component = connected_component(nodes, v)
                row.append(component)
            else:
                row.append(0)
        C.append(row)
    for u in range(len(clusters)):
        for v in range(u+1,len(clusters)):
            for w in range(v+1,len(clusters)):
                    if C[u][v]!= 0 and C[u][w]!= 0 and C[w][v]!= 0:
                        if C[u][v]== C[u][w] and C[v][u]== C[v][w] and C[w][u]== C[w][v]:
                            return False
    return True

                              
if task == "lexbfs":
    print(lexbfs(clusters)) 
elif task == "chordal":
    lexicographic= lexbfs(clusters)
    l = lexicographic[::-1]
    print(chordal(l))
elif task == "interval":
    lexicographic= lexbfs(clusters)
    l = lexicographic[::-1]
    ischordal= chordal(l)
    if ischordal:
        isinterval= (interval())
        print(isinterval)
    else:
        print(False)
