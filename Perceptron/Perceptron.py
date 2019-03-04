import numpy as np

def perceptron(X,Y,r,T):
    w = [0]*len(X[0])
    e = 0
    cont = True
    for e in range(T):
        for i,x in enumerate(X):
            if np.sign(np.dot(x,w)) * Y[i] <= 0:
                e += 1
                w = w + r*Y[i]*x
                # if e >= T:
                #     cont = False
                #     break

    return w

def votedperceptron(X,Y,r,T):
    w = [np.zeros(len(X[0]))]
    c = [0]
    m = 0
    cont = True
    for e in range(T):
        for i,x in enumerate(X):
            if Y[i]*np.dot(w[m],x) <= 0:
                w.append(w[m] + r * Y[i] * x)
                m += 1
                c.append(1)
            else:
                c[m] += 1
    return w,c

def averageperceptron(X,Y,r,T):
    w = np.zeros(len(X[0]))
    a = np.zeros(len(X[0]))
    e = 0
    cont = True
    for e in range(T):
        for i,x in enumerate(X):
            if Y[i]*np.dot(w,x) <= 0:
                w = w + r * Y[i] * x
            a = a + w
    return a

def evalvotedperceptron(w,c,x):
    sum = 0
    for i, wi in enumerate(w):
        sum += c[i] * np.sign(np.dot(wi, x))
    return np.sign(sum)
