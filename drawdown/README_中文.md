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
