import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(2431)

class Model(object):
    def __init__(self, length=500, width=500, sur=5, threshold=3, empty_ratio=0.9, race_ratio=0.7):
        # empty_ratio: the ratio of empty houses(point)
        # race_ration: the ratio of the bigger group, range(0.5,1)
        self.length = length
        self.width = width
        # relocate condition 
        self.sur = sur             
        self.threshold = threshold
        # use red and blue to represent two groups
        self.red = 1
        self.blue = 2
        # denote red race leader as -1, blue as -2 
        self.yellow = -1
        self.green = -2
        self.empty = 0
        # generate the initial distribution
        v=np.zeros((length)*(width)) 
        n1 = int((1-empty_ratio)*race_ratio*(length)*(width))
        n2 = int((1-empty_ratio)*(1-race_ratio)*(length)*(width))
        for i in range(n1):
            v[i]=1
        for j in range(n2):
            v[n1+j]=2
        v[0] = -1
        v[1] = -1
        v[n1+1] = -2
        v[n1] = -2
        random.shuffle(v)
        self.matrix = v.reshape((length,width))
        self.population = n1+n2
    
    # judge whether agent should relocate
    def is_satisfied(self, i, j, kind):
        neighbour = 0
        same_neighbour = 0
        n = 1
        leader = 0
        while(neighbour<self.sur):
            p=max(-n,-i)
            while p <= n and p+i<self.length:
                if p==n | p==-n:
                    if self.matrix[i+p][j]>0:
                        neighbour += 1
                        if -self.matrix[i+p][j]==kind:
                            leader=1
                            break
                        if self.matrix[i+p][j]==kind:
                            same_neighbour += 1
                        if neighbour==self.sur:
                            break
                else:
                    if j+n-p<self.width:
                        if self.matrix[i+p][j+n-p]>0:
                            neighbour += 1
                            if -self.matrix[i+p][j]==kind:
                                leader=1
                                break
                            if self.matrix[i+p][j+n-p]==kind:
                                same_neighbour += 1
                            if neighbour==self.sur:
                                break
                    if j-n+p>=0:
                        if self.matrix[i+p][j-n+p]>0:
                            neighbour += 1
                            if -self.matrix[i+p][j]==kind:
                                leader=1
                                break
                            if self.matrix[i+p][j-n+p]==kind:
                                same_neighbour += 1
                            if neighbour==self.sur:
                                break
                p += 1
                if neighbour==self.sur:
                    break
            n += 1
        # if the fraction of the same group < the desired fraction
        # or no-one live nearby, then relocate
        # 2% agent will relocate due to other reason 
        rr=np.random.choice((0,1),p=(0.02,0.98))
        if leader == 1:
            return True
        elif same_neighbour >= self.threshold:
            if rr == 1:
                return True
            else:
                return False
        else:
            return False
    
    # find the empty space
    def random_find(self):
        i = random.randint(0,self.length-1)
        j = random.randint(0,self.width-1)
        while self.matrix[i][j] != 0:
            i = random.randint(0, self.length - 1)
            j = random.randint(0, self.width - 1)
        return (i,j)
    
    # realize the relocate progress and calculate the number of unsatisfied agents
    def move(self):
        satisfy = 0
        for i in range(self.length):
            for j in range(self.width):
                if self.matrix[i][j] > 0:
                    people_kind = self.matrix[i][j]
                    judge = self.is_satisfied(i,j,people_kind)
                    if judge == 0:
                        (p,q) = self.random_find()
                        self.matrix[p][q] = people_kind
                        self.matrix[i][j] = self.empty
                    else:
                        satisfy += 1
        unsatisfy = self.population-satisfy
        return unsatisfy
    
    # plot the distribution of two groups
    def draw(self,time,unsatisfy=0):
        redx = []
        bluex = []
        yellowx = []
        greenx = []
        redy = []
        bluey = []
        yellowy = []
        greeny = []
        for i in range(self.length):
            for j in range(self.width):
                if self.matrix[i][j] == self.blue:
                    bluex.append(i)
                    bluey.append(j)
                elif self.matrix[i][j] == self.red:
                    redx.append(i)
                    redy.append(j)
                elif self.matrix[i][j] == self.yellow:
                    yellowx.append(i)
                    yellowy.append(j)
                elif self.matrix[i][j] == self.green:
                    greenx.append(i)
                    greeny.append(j)
        plt.figure(figsize=(12,12))
        plt.scatter(redx,redy,c = 'r',marker='.',linewidths=0)
        plt.scatter(bluex,bluey,c = 'b',marker='.',linewidths=0)
        plt.scatter(yellowx,yellowy,c = 'y',marker='.',linewidths=10)
        plt.scatter(greenx,greeny,c = 'g',marker='.',linewidths=10)
        if time==0:
            plt.title('Initial')
        else:
            print('Round:'+str(time),'move people:'+str(unsatisfy))
            title = 'Round:'+str(time)+' move-people:'+str(unsatisfy)
            plt.title(title)
        plt.show()

# draw the progress
if __name__ == '__main__':
    l = 500
    w = 500
    empty_r = 0.9
    race_r = 0.7
    s = 5
    t = 3
    s = Model(length=l, width=w, 
              sur=s, threshold=t,
              empty_ratio=empty_r,
              race_ratio=race_r)
    s.draw(0)
    stop = 30
    unsatisfy = 1
    move_list=[]
    i = 0
    while(unsatisfy>0 and i<stop):
        unsatisfy = s.move()
        move_list.append(unsatisfy)
        i+=1
        s.draw(i,unsatisfy)
    plt.figure(figsize=(18,6))
    plt.bar(range(1,i+1),move_list)
    plt.title("Numbers of relocate agents for each round")
    plt.xlim([0.5,i+1])
    plt.xlabel("Round")
