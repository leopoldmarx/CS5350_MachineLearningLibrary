
import numpy as np

class Tree(object):
    def __init__(self):
        self.children = []
        self.attribute = []

    def addChild(self, node):
        self.children.append(node)

    def setAttribute(self, str):
        self.attribute = str

    def printDepth(self):
        print(self.attribute)
        for i in range(len(self.children)):
            c = self.children[i]
            if type(c) == type(Tree()):
                c.printDepth1(1)


    def printDepth1(self,indent):
        print(' '*indent + self.attribute.__str__())
        for i in range(len(self.children)):
            c = self.children[i]
            if type(c) == type(Tree()):
                c.printDepth1(indent+1)


def evaluateID3(tree,data,columns,bool):
    #if type(tree.attribute) == type(None):
    for t in tree.children:
        col = np.where(columns == t.attribute[0])
        #print(t.attribute)
        #print(col)
        col = col[0]
        #print(col)
        if len(col) == 1:
            col = col[0]
            if t.attribute[1] == data[col]:
                if bool:
                    print(t.attribute)
                return evaluateID3(t,data,columns,bool)
        else:
            if bool:
                print(t.attribute)
            return t.attribute
    #else:
        # col = np.where(columns==tree.attribute[0])
        # col = col[0][0]
        # for t in tree.children:
        #     print(t.attribute)
        #     print(t)
        #     att = t.attribute[0]
        #     if t.attribute == data[col]:
        #         print (t.attribute)


def ID3(S,attributes,label,columns,g,depth):
    root = Tree()

    if depth <= 0 or len(attributes) <=0:
        count = [0] * len(label)
        for i in range(len(S)):
            index = label.index(S[i, -1])
            count[index] = count[index] + 1
        maxcount = -1
        maxLabel = -1
        for i in range(len(count)):
            if maxcount < count[i]:
                maxcount = count[i]
                maxLabel = i
        child = Tree()
        child.setAttribute(label[maxLabel])
        root.addChild(child)
        return root

    i1 = S[0,-1]
    broke = False
    for i in range(len(S)):
        if S[i,-1] != i1:
            broke = True
            break

    if (not(broke)):
        #TODO: create leaf node with label

        #root.setAttribute(i1)
        child = Tree()
        child.setAttribute(i1)
        root.addChild(child)
        return root
    else:
        #TODO: create root node for tree
        bestAttribute = -1
        highestGain = -1
        for i in range(len(attributes)):
            g = g.lower()
            if g == 'entropy':
                gain = entropyGain(S,i,attributes[i],label)
            elif g == 'me':
                gain = MEGain(S,i,attributes[i],label)
            elif g == 'gini':
                gain = giniGain(S,i,attributes[i],label)
            if gain>highestGain:
                bestAttribute = i
                highestGain=gain
        size = len(attributes[bestAttribute])
        for v in attributes[bestAttribute]:
            #TODO: add new branch with attribute = v
            #TODO: Sv = S with attributes = v
            Sv = skim(S,bestAttribute,v)
            if(Sv == -1):
                #TODO add leaf node with highest count label
                count = np.zeros(len(label))
                for i in range(len(S)):
                    index = label.index(S[i, -1])
                    count[index] = count[index] + 1
                maxlabel = -1
                maxVal = -1
                for i in range(len(label)):
                    if count[i] >= maxVal:
                        maxVal = count[i]
                        maxlabel = i
                child = Tree()
                child.setAttribute(label[maxlabel])
                root.addChild(child)
                return root
            else:
                #TODO: add subtree with ID3(Sv,attributes.remove(attribute)
                #print(columns[bestAttribute] +'='+ v)
                # print(attributes)
                # print(np.delete(attributes,(bestAttribute),axis=0))
                child = ID3(Sv,np.delete(attributes,(bestAttribute)),label,np.delete(columns,(bestAttribute)),g,depth-1)
                child.setAttribute([columns[bestAttribute],v])
                root.addChild(child)
        return root


def entropyGain(S,col,attributes,label):
    gain = entropy(S,label)
    count = np.zeros(len(attributes))
    for i in range(len(S)):
        index = attributes.index(S[i,col])
        count[index] = count[index] + 1
    for i in range(len(attributes)):
        a = attributes[i]
        s_a = skim(S,col, a)
        if s_a != -1:
            gain = gain - count[i]/len(S) * entropy(s_a,label)
    return gain

def entropy(S,label):
    e = 0
    count = [0]*len(label)
    for i in range(len(S)):
        index = label.index(S[i,-1])
        count[index] = count[index] + 1

    for i in range(len(label)):
        if count[i] != 0:
            p = count[i]/len(S)
            e = e - p*np.log(p)

    return e


def ME(S, label):
    count = [0] * len(label)
    for i in range(len(S)):
        index = label.index(S[i, -1])
        count[index] = count[index] + 1
    maxcount = -1
    for i in range(len(label)):
        if maxcount < count[i]:
            maxcount = count[i]

    return (len(S)-maxcount)/len(S)


def MEGain(S,col,attributes, label):
    gain = ME(S, label)
    count = np.zeros(len(attributes))
    for i in range(len(S)):
        index = attributes.index(S[i, col])
        count[index] = count[index] + 1
    for i in range(len(attributes)):
        a = attributes[i]
        s_a = skim(S, col, a)
        if s_a != -1:
            gain = gain - count[i] / len(S) * ME(s_a, label)
    return gain

def Gini(S,label):
    count = [0] * len(label)
    for i in range(len(S)):
        index = label.index(S[i, -1])
        count[index] = count[index] + 1
    sum = 1
    for i in range(len(count)):
        sum = sum - np.power((count[i]/len(S)),2)

    return sum


def giniGain(S,col,attributes, label):
    gain = Gini(S, label)
    count = np.zeros(len(attributes))
    for i in range(len(S)):
        index = attributes.index(S[i, col])
        count[index] = count[index] + 1
    for i in range(len(attributes)):
        a = attributes[i]
        s_a = skim(S, col, a)
        if s_a != -1:
            gain = gain - count[i] / len(S) * Gini(s_a, label)
    return gain

def skim(S,col,att):
    s_a = -1
    count = 0
    #TODO: if S[i,col == att, add tot s_a,
    for i in range(len(S)):
        if S[i,col] == att:
            if s_a == -1:
                s_a = np.array([S[i,:]])
            else:
                s_a = np.vstack((s_a,S[i,:]))
    return np.delete(s_a,(col),1)