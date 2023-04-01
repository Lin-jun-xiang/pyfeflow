## :penguin:FEFLOW-PYTHON

- **所需軟體**
    - `FEFLOW`: 地下水流數值模擬 (免費版或付費版)
    - `Python`

* **功能大綱**
    - [抽水洩降可視化](./drawdown/)
    - [*蒙地卡羅* 數值模擬](./mc/)
    - [*馬可夫鏈蒙地卡羅* 數值模擬](./mcmc/)
    - [*自動優化(校正)* 模擬](./optimization/)

---

### 介紹

本專案會透過 `ifm-api-python` 開發地下水流數值模擬的套件。

> 什麼是 `ifm-api` ?
> 介面管理 (Interface Manager) 是 `feflow` 中的一種內置函數 (`api`)，通過腳本 (ex: `python`, `c++`) 調用這些函數可以操作整個模擬過程，實現更精細和自動化的數值模擬。
>舉例來說，如果要進行上萬次模擬，手動透過 `feflow GUI` 反覆操作是不現實的，但是通過腳本操作就可以寫一個程序來實現上萬次模擬，並把每次模擬結果存取下來。

---

### 使用方式

1. 點選該專案 :star:`Star`，給予開發者支持與動力

2. 確保自己電腦有 `feflow`、`python` 程式

3. 透過功能大綱連結至該功能詳細介紹與開源碼

    * 各功能的介紹都會先說明 `feflow` 是否需要 `license`

    * 各功能都會有詳細說明檔案 (`README.md`)

4. 進行 `git clone https://github.com/Lin-jun-xiang/feflow-python-ifm.git`

5. 開始使用

<a href="#top">Back to top</a>
