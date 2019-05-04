# coding: utf-8

import numpy as np

T=200000 # 20000 users need to be served
arate=1 # arrival rate
drate=1 # departure rate

t=0 # 时刻/时间
arrival=[] # 模拟到达

while t < T:
    t = t + np.random.exponential(1.0/arate)
    arrival.append(t)

t=0 
N=0 # states (节点) 系统里所有人数（等待的和服务的）
departure=[]
recording=[] # 记录服务的起止时间和当时等待人数（等待人数须不大于容量）


# len(departure[]) 不可以超过10， N 不可以超过10 
#  先 N+1 或 N-1 之后再去检验 N 是否大于10
#  
#  departure[] 长度<5时，队列未满，所以是drate*len(departure)
#  departure[] 长度>=5时，队列满，所以时drate*5

while (t<T and len(arrival)>0):  
    if len(departure)==0:          # 离开队列为0，等待到达
        told=t                     # 服务的开始时刻
        t=arrival[0]               # 到达时间
        del arrival[0]                
        de=t+np.random.exponential(1.0/drate) # 离开时间 t + 随机
        departure.append(de)
        recording.append([told,t,N])
        N=N+1
    else:  # 队列里是有人的
        # 在下一个到达前先离去
        if departure[0]<arrival[0]: # 排队的人减少,不需要排队， N=N-1
            told=t                  # 开始时刻
            t=departure[0]          # 前一个的离去时刻
            del departure[0]        
            recording.append([told,t,N]) # 记录 前一个离去时刻，下一个离去时刻，两者之差为服务时间
            N=N-1                       # 队列减一
            
            if N>=1 and N<5:                # 如果队列不为空，算出下一个离去的时间
                de=t+np.random.exponential(1.0/(N*drate))  
                departure.append(de)
                departure.sort()  # 从小到大排序，小时刻先出
            elif N>=5 and N<=10:
                de=t+np.random.exponential(1.0/(5*drate))  
                departure.append(de)
                departure.sort()# 从小到大排序，小时刻先出

        # 在下一个到达后再离去
        else:                   # 排队的人增加,需要排队，队列加长 N=N+1
            if N>=10:
                told=t
                t=arrival[0]
                del arrival[0]
                recording.append([told,t,N])
            else:
                told=t
                t=arrival[0]
                del arrival[0]
                recording.append([told,t,N])
                N=N+1
                del departure[0]

                if N>=2 and N<5:                # 如果队列不为空，算出下一个离去的时间
                    de=t+np.random.exponential(1.0/(N*drate))  
                    departure.append(de)
                    departure.sort()  # 从小到大排序，小时刻先出
                elif N>=5 and N<=10:
                    de=t+np.random.exponential(1.0/(5*drate))  
                    departure.append(de)
                    departure.sort()  # 从小到大排序，小时刻先出

print recording[1:100]

duration=[]
x1=0.0
x2=0.0
for i in range(0, len(recording)):
    x1=x1+(recording[i][1]-recording[i][0])*recording[i][2]  # 所有客户总等待时间
    x2=x2+(recording[i][1]-recording[i][0])                  # 总服务时间


Mnumber=[x[2] for x in recording] # 取每一条 recording[] 的第三条数据，即等待人数
M=max(Mnumber) # 队列的最大长度/同时等待时的最多人数
print(M)

distribution=[0 for i in range(M+1)]  # 一个长为 M+1 的全0的list（初始化）

print len(distribution)


for i in range(0, len(recording)):
    state=recording[i][2] # state = 等待人数 （每一个recording的第三项，即等待人数）
    distribution[state]=distribution[state]+recording[i][1]-recording[i][0] # 在N人等待时的等待时间之和
    
print distribution

meanqueue=x1/x2  # 平均队长
print (meanqueue) 
sumtime=sum(distribution) # 在每个节点下的等待时间
pdf=[x/sumtime for x in distribution] 
print pdf