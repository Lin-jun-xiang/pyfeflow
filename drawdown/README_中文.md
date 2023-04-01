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
