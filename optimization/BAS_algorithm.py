import time
import math
import pandas as pd
import sys
import ifm
import numpy as np

"""
天牛須演算法 (Beetle Antennae search algorithm, BAS)
以抽水量未知問題，n口井即n個未知參數(抽水量)or"n維度問題"
hyper-parameters : d0, effected_radius
優點 : (1)運算量小 (2)具有全局解 (3)代碼容易實現
相關概念參考:https://zhuanlan.zhihu.com/p/30742461
"""
sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
doc = ifm.loadDocument('D:\\FEM_FILE\\Simulation\\new_gp_MultipleWell.fem')

def normalize(x):
    norm = math.sqrt(sum(e**2 for e in x))
    return x / norm

def set_obs_heads(data):
    obs_heads = {}
    for i in data.index:
        obs_heads[i+1] = data["ObsHead"][i]

    return obs_heads

def set_obs_coordinates(data):
    obs_x, obs_y = {}, {}
    for i in data.index:
        obs_x[i+1] = data["X"][i]
        obs_y[i+1] = data["Y"][i]

    return obs_x, obs_y

def get_well_effect_region(well_number, obs_x, obs_y, effect_radius=1000):
    well_node = doc.getMultiLayerWellTopNode(well_number)
    well_x, well_y = obs_x[well_node], obs_y[well_node]

    effected_nodes = []
    for node in obs_x:
        distance = ((well_x - obs_x[node])**2 + (well_y - obs_y[node])**2)**0.5

        if distance <= effect_radius:
            effected_nodes.append(node)
    return effected_nodes

def sign(a):
    if a > 0: return 1
    elif a < 0: return -1
    else: return 0

def optimizing_function(obs_heads, effected_nodes, well_numbers, well_pumps_rate):
    for well_number in range(well_numbers):
        doc.setMultiLayerWellAttrValue(well_number, 0, well_pumps_rate[well_number])

    loss = 0
    N = len(effected_nodes)
    doc.startSimulator()

    for node in effected_nodes:
        sim_head = doc.getResultsFlowHeadValue(node-1)
        loss += (obs_heads[node] - sim_head)**2/N # MSE
    doc.stopSimulator()

    return loss

def get_well_info():
    well_n = int(doc.getNumberOfMultiLayerWells())
    print("well number= ", well_n)
    for i in range(well_n):
        print(f"doc.setMultiLayerWellAttrValue({i}, 0, {int(doc.getMultiLayerWellAttrValue(i, 0))})")

time_start=time.time()

path = 'D:\\VSCode\\Excel_py\\'
data = pd.read_excel(path + "new_gp_Aq1ObsHead.xlsx")

obs_heads = set_obs_heads(data)
obs_x, obs_y = set_obs_coordinates(data)[0], set_obs_coordinates(data)[1]

well_numbers = doc.getNumberOfMultiLayerWells()

well_pumps_rate = np.array([0 for _ in range(well_numbers)]) # 待解參數，即n口井各自的抽水量(n維度問題)
xl = well_pumps_rate
xr = well_pumps_rate

effected_nodes = []
for well_number in range(well_numbers):
    effected_nodes.extend(get_well_effect_region(well_number, obs_x, obs_y))

# Algorithm
iter = 500
step = 250
d0 = 5000
i = 0

while step/100 >= 2 or i <= iter: # 2即為可接受的loss值(水頭總誤差)
    dir = np.random.randn(well_numbers)
    dir = normalize(dir)
    xl = well_pumps_rate + d0*dir/2
    xr = well_pumps_rate - d0*dir/2

    fl = optimizing_function(obs_heads, effected_nodes, well_numbers, xl)
    fr = optimizing_function(obs_heads, effected_nodes, well_numbers, xr)

    well_pumps_rate = well_pumps_rate - step*dir*sign(fl-fr)
    step = 100 * 0.5 * (abs(fl) + abs(fr)) # 根據水頭誤差值大小判斷下次抽水量變動大小
    i += 1
    print('epoch=', i+1, 'loss=', fl, fr, 'step=', step)

time_end=time.time()

get_well_info()
print('time cost',time_end-time_start,'s')
print("Finished")
