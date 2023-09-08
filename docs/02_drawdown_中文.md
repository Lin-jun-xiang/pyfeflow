# Drawdown Visualization

### 簡介

* 地下水位洩降 (Drawdown): 抽水前與抽水後的地下水位差異

* 計算水位洩降方式:
    * (抽水前的水位) 減去 (抽水後的水位)

* 使用工具
    * 數值地下水模擬工具：FEFLOW 7.3

    * 腳本語言：Python 3.8.6

* 程式原理
    1. 利用 `ifm` 取出當前水頭值 (`doc.getResultsFlowHeadValue()`)
    2. 設置抽水率，並進行模擬
    3. 取出抽水後的水頭值
    4. 利用 (抽水前水頭值) 減去 (抽水後水頭值)

---

### 範例

1. `ifmDrawdown.py` 計算出 `drawdown.xlsx` 如下:
    | Node | Drawdown |
    | ---- | -------- |
    |1|0.000639|
    |2|0.001099|
    |3|0.007327|
    |...|...|

2. 執行完程式，於 `feflow` GUI 中:
    * `User Data`
 
        ![](../images/2023-04-03-16-41-50.png)

3. 可視化洩降

   <p align=center>
   <image src="https://user-images.githubusercontent.com/63782903/229460648-27bd0a51-1e2d-4d38-ac1e-21d49c0a4b34.png" width=50%>
      </p>

```python
# ifmDrawdown.py
import sys

import ifm
import pandas as pd


# Adding FEFLOW directory to system path
sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")

# Loading FEFLOW project document
doc = ifm.loadDocument('Your_FEM_FILE')

# Get the Nodes in fem
nodes = doc.getNumberOfNodes()

# Get the initial head for each node
init_heads = [doc.getResultsFlowHeadValue(node) for node in range(nodes)]

# Start simulation with pumping
doc.startSimulator()

# Get the head for each node after pumping
pump_heads = [doc.getResultsFlowHeadValue(node) for node in range(nodes)]

# Calculate the "drawdown"
drawdown = [init_head - pump_head for init_head, pump_head in zip(init_heads, pump_heads)]


def create_user_data(user_data_name: str):
    try:
        # Enable reference distribution recording
        bEnable = 1 # disable = 0, enable = 1

        # Create "user data"
        if doc.getNodalRefDistrIdByName(user_data_name) == -1:
            doc.createNodalRefDistr(user_data_name)

        user_data = doc.getNodalRefDistrIdByName(user_data_name)
        doc.enableNodalRefDistrRecording(user_data, bEnable)

    except Exception as err:
        print(err)

    return user_data


def set_user_data():
    for nNode in range(nodes):
        doc.setNodalRefDistrValue(rID_draw, nNode, pump_heads[nNode])

rID_draw = create_user_data("drawdown")
set_user_data()

doc.stopSimulator()
doc.saveDocument()

# Writing the drawdown data to xlsx
df = pd.DataFrame({
    "Node": [node+1 for node in range(nodes)],
    "Drawdown": drawdown
})

df.to_excel("..//Excel//Drawdown.xlsx", index=False)
```
