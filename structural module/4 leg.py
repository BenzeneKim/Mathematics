import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def PositionVec1(Base, Plength, Alength):
    X = np.zeros((2,1))
    X[0] = (Plength**2 - Alength**2 + Base**2)/(2*Base)
    X[1] = np.sqrt(Plength**2 - X[0]**2)
    return X

def PositionVec2(Base, Plength, Alength):
    X = np.zeros((2,1))
    X[0] = (Plength**2 - Alength**2 + Base**2)/(2*Base)
    X[1] = -np.sqrt(Plength**2 - X[0]**2)
    return X

def NewPointVector1(Pivot, Arm, Plength, Alength):
    Pvec = Arm - Pivot
    Base = lin.norm(Pvec)
    Pvec /= Base
    
    #Position Vector in transformed domain
    PosVec = PositionVec1(Base, Plength, Alength)
    
    #Rotation Tensor
    Pvec90 = np.roll(Pvec, 1)
    Pvec90[0] = -Pvec90[0]
    
    RotTen = np.hstack([Pvec, Pvec90])
    
    return np.matmul(RotTen, PosVec) + Pivot

def NewPointVector2(Pivot, Arm, Plength, Alength):
    Pvec = Arm - Pivot
    Base = lin.norm(Pvec)
    Pvec /= Base
    
    #Position Vector in transformed domain
    PosVec = PositionVec2(Base, Plength, Alength)
    
    #Rotation Tensor
    Pvec90 = np.roll(Pvec, 1)
    Pvec90[0] = -Pvec90[0]
    
    RotTen = np.hstack([Pvec, Pvec90])
    
    return np.matmul(RotTen, PosVec) + Pivot

theta = np.zeros(2)
theta[1] = np.pi

fig, ax = plt.subplots(figsize = (12,6))

ax.set_xlim(-150, 150)
ax.set_ylim(-100, 50)

Points1 = np.zeros((2,2,8))
Points2 = np.zeros((2,2,8))

graphs_set = [[ax.plot([], [], color = 'C0')[0] for i in range(11)] for j in range(2)]

'''
Seqence - (PivotInd, ArmInd, PivotLen, Armlen)
'''
Sequence = [(1,2,41.5,50.0), (2,1,61.9,39.3),
           (1,3,40.1,55.8), (4,5,36.7,39.4),
           (4,6,49.0,65.7)]

Points1[:,:,0] = Points2[:,:,0] = [[0, 7.8] for i in range(2)]
Points1[:,:,1] = [[-38.0, 0] for i in range(2)]
Points2[:,:,1] = -Points1[:,:,1]

def Animated(*args):
    global theta
    theta += np.pi/30
    
    Points1[0,:,2] = Points1[0,:,0] + [np.cos(theta[0]) * 15, np.sin(theta[0]) * 15]
    Points1[1,:,2] = Points1[1,:,0] + [np.cos(theta[1]) * 15, np.sin(theta[1]) * 15]
    Points2[:,:,2] = Points1[:,:,2]
    
    graphs_set[0][0].set_data(Points1[0,0,(0,2)], Points1[0,1,(0,2)])
    graphs_set[1][0].set_data(Points1[1,0,(0,2)], Points1[1,1,(0,2)])
    
    for i in range(5):
        PInd, AInd, Plen, Alen = Sequence[i]
        
        for j in range(2):
            NP1 = NewPointVector1(Points1[j,:,PInd].reshape(-1,1), Points1[j,:,AInd].reshape(-1,1), Plen, Alen)
            NP2 = NewPointVector2(Points2[j,:,PInd].reshape(-1,1), Points2[j,:,AInd].reshape(-1,1), Plen, Alen)
            Points1[j,:,i+3] = NP1.reshape(-1)
            Points2[j,:,i+3] = NP2.reshape(-1)
            graphs_set[j][2*i+1].set_data(Points1[j,0,(PInd, i+3, AInd)], Points1[j,1,(PInd, i+3, AInd)])
            graphs_set[j][2*i+2].set_data(Points2[j,0,(PInd, i+3, AInd)], Points2[j,1,(PInd, i+3, AInd)])
        
        graphs = graphs_set[0] + graphs_set[1]
    
    return graphs

anim = animation.FuncAnimation(fig, func = Animated, frames = 900, interval = 17, blit = True)
anim.save("4 leg walking.mp4", fps = 60, dpi = 72)

plt.show()