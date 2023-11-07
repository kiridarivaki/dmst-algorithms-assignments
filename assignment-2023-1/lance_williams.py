import argparse

parser = argparse.ArgumentParser()
parser.add_argument('method', choices=[
                    'single', 'complete', 'average', 'ward'], nargs=1)
parser.add_argument('datafilename')
obj = parser.parse_args()
file = open(obj.datafilename)
cl = file.read().split()
clusters = [int(x) for x in cl]
clusters.sort()
t_len= {}   #dictionary t_len[key= length of t, value= merged cluster u(s, t)]

def distance(u, v):
    
    if isinstance(u, list) and len(u)== 1:
        u= u[0]
    if isinstance(v, list) and len(v)== 1:
        v= v[0]
    if not(isinstance(u, list)) and not(isinstance(v,list)):
        return abs(u-v)
    
    method = obj.method[0]
    if method == 'single':
        ai, aj, b, g = 0.5, 0.5, 0, -0.5
    elif method == 'complete':
        ai, aj, b, g = 0.5, 0.5, 0, 0.5
    elif method == 'average':
        b, g = 0, 0
    elif method == 'ward':
        g = 0

    if isinstance(v, list) and not(isinstance(u, list)):
        u, v= v, u
    if isinstance(u, list) and len(u)== 2:
        s= u[0]
        t= u[1] 
    if (isinstance(u, list) and len(u)> 2):
        k= 0
        for key, value in t_len.items():    #searching for len(t) in the dictionary, this indicates where to split u to s and t
            if u in value:
                k= key
                break
        s= u[0:len(u)-k]
        t= u[len(s):len(u)]

    if method== 'average' or method== 'ward':
        if isinstance(s, list):
            s2= len(s)
        else:
            s2= 1
        if isinstance(t, list):
            t2= len(t)
        else:
            t2= 1
        if isinstance(v, list):
            v2= len(v)
        else:
            v2= 1
        if method == 'average':
            ai = s2/(s2+t2)
            aj = t2/(s2+t2)
        else:
            ai = (s2+v2)/(s2+v2+t2)
            aj = (t2+v2)/(s2+v2+t2)
            b = -v2/(s2+v2+t2)
    d1= distance(s, v)
    d2= distance(t, v)
    if method== 'average':
        d= ai*d1+aj*d2+g*abs(d1-d2)
    else:
        d3= distance(s, t)
        d= ai*d1+aj*d2+b*d3+g*abs(d1-d2)
    return d

def custom_sort(cell):
    if isinstance(cell, list):
        return cell[0]
    else:
        return cell

def hierarchical_clustering(x, y, clusters, min_dist):
    u_list = isinstance(x, list)
    v_list = isinstance(y, list)
    if u_list:
        merged_clusters= len(x)   
        print(f'({" ".join(str(k) for k in x)})', end=' ')
    else:
        merged_clusters= 1
        print(f'({x})', end= ' ')
    if v_list:
        merged_clusters+= len(next_cluster)   
        print(f'({" ".join(str(k) for k in y)})', end=' ')
    else:
        merged_clusters+= 1
        print(f'({y})', end= ' ')
    print(f'{min_dist:.2f} {merged_clusters}')
    
    if isinstance(x, list):
        x2= x[:]
    if isinstance(y, list):
        y2= y[:]
    clusters.remove(x)
    clusters.remove(y) 

    if isinstance(x, list) and not(isinstance(y, list)):
        x2.append(y)
        clusters.append(x2)
    elif isinstance(x, list) and isinstance(y, list):
        clusters.append(x+y)
    elif not(isinstance(x, list)) and isinstance(y, list):
        y2.append(x)
        clusters.append(y2)
    else:
        clusters.append([x, y])                                                                                                                       
    clusters.sort(key= custom_sort)
    return clusters

done= False
l= len(clusters)
count= 0
while not(done):
    min_dist= float('inf')
    for i in range(len(clusters)-1):
        j= i+1
        while j<= len(clusters)-1:
            dist= distance(clusters[i], clusters[j])
            if dist<min_dist:
                min_dist= dist
            j+= 1
    for x in range(l-1):
        if x< l-1:
            c= clusters[x]
            y= x+1
            while y<= len(clusters)-1:
                next_cluster= clusters[y]
                dist= distance(c, next_cluster)
                merged= 0
                while dist== min_dist and y< l:
                    clusters= hierarchical_clustering(c, next_cluster, clusters, min_dist)
                    merged+= 1
                    l= len(clusters)
                    if l==1:
                        break
                    c= clusters[x]
                    if isinstance(next_cluster, list):
                        if len(next_cluster) in t_len:
                            t_len[len(next_cluster)].append(c)
                        else:
                            t_len[len(next_cluster)]= [c] 
                    elif isinstance(c, list) and not(isinstance(next_cluster, list)):
                        if 1 in t_len:
                            t_len[1].append(c)
                        else:
                            t_len[1]= [c]
                    y+= 1
                    if y< l:
                        next_cluster= clusters[y]
                        dist= distance(c, next_cluster)
                if merged>= 1:
                    y= x+1
                else:    
                    y+= 1
        if l== 1:
            done= True
