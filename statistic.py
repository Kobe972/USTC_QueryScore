import numpy as np
import matplotlib.pyplot as plt
from math import *
import pandas as pd
with open('data.txt','r',encoding='utf-8') as fp:
    lines=fp.readlines()
scores=[]
datalist=[]
for line in lines:
    score=line.split(' ')[-1]
    scores.append(float(score))
    datalist.append([line.split(' ')[0],float(score)])
datalist=pd.DataFrame(np.array(datalist))
datalist.columns=['StuId','Score']
datalist.to_csv('scores.csv',index=None)
space=5 #直方图中5分划一段
minimum=floor(min(scores))-floor(min(scores))%space
maximum=ceil(max(scores))+space-ceil(max(scores))%space
bins=[minimum+i*5 for i in range(int((maximum-minimum)/5))]
plt.hist(scores,bins=bins,rwidth=0.9)
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.savefig('hist.png')
print('总人数：',len(scores))
print('平均分：',sum(scores)/len(scores))
print('最高分：',max(scores))
print('最低分：',min(scores))
scores.sort()
print('中位数：',scores[int(len(scores)/2)])
print('前百分之40分数：',scores[int(len(scores)/10*6)])
print('前百分之30分数：',scores[int(len(scores)/10*7)])
print('前百分之20分数：',scores[int(len(scores)/10*8)])
print('前百分之10分数：',scores[int(len(scores)/10*9)])
