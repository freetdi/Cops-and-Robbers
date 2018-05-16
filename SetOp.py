import copy

def isEmpty(X):
    return len(X) == 0

def emptySet():
    return []

def add(X, Y):
    tmp = copy.deepcopy(X)
    for i in range(0, len(Y)):
        if Y[i] not in tmp:
            tmp.append(Y[i])
    return tmp

def intersection(X, Y):
    tmp = list()
    for i in range(0, len(X)):
        for j in range(0, len(Y)):
            if(X[i] == Y[j] and X[i] not in tmp):
                tmp.append(X[i])
    return tmp
    
def difference(X, Y):
    indx = list()
    tmp = list()
    for i in range(0, len(Y)):
        for j in range(0, len(X)):
            if X[j] == Y[i]:
                indx.append(j)
    for i in range(0, len(X)):
        if(i not in indx):
            tmp.append(X[i])
    return tmp

#bubble :)
def sort(X):
    for i in range(0, len(X)):
        for j in range(0, len(X)-i-1):
            if(X[j] > X[j+1]):
                tmp = X[j+1]
                X[j+1] = X[j]
                X[j] = tmp
    return X
