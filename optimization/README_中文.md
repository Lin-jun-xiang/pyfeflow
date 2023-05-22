# Optimization-by-BAS
### 簡介
* 使用天牛鬚搜索演算法（Beetle Antennae Search algorithm，簡稱BAS）解決地下水模擬中的未知參數問題 (降低模擬誤差)
* 使用工具

    * 數值地下水模擬工具：FEFLOW 7.3

    * 腳本語言：Python 3.8.6

* 功能與目的
    * 建立地下水流模型需要**模擬值與觀測值擬和**，但有時會因缺少資料而無法達成。
    * **優化演算法**可以**自動調整參數**，達到擬和目的。
    * 該功能可以透過優化算法找到缺少的資料參數，使模擬值與觀測值擬和。

* **優化演算法 (最佳化)** vs `FePEST` 校正:
   * 優化算法能夠自定義目標函數，使得模擬結果可以更快、更容易擬和
   * 優化算法不侷限於特定參數，可適用任何未知參數的優化 (e.g. `FePEST` 只能校正 `element` 的屬性，無法校正抽水井參數)

* `BAS` 是2017年由 Jiang 和 Li 開發的，屬於**優化演算法 (最佳化)** 的一種，演算法如下：

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159463464-716ea7a1-7af6-491e-aebd-db98ea735cd2.png" width=50%/>
</p>

* 應用情境
在我們的研究區域中，有許多私人井，我們無法取得詳細資訊（例如：井位、抽水率等）。因此，我們在研究區域中均勻設置一些虛擬井，所有抽水率都是我們系統的參數。這些系統參數將透過`BAS`進行調整，並且使模擬值與觀測值擬和。
(PS: 可以把未知參數視為水力傳導係數、孔隙率、飽和度...等)

* :warning: **重要提醒**: 該應用情境為參考論文 - <a href="https://hdl.handle.net/11296/tq3m78" target="_blank">**伏流水資源開發與評估數值模擬－ 以高屏溪為例**</a>

---
### 演算流程

* 定義以下:
    * **未知參數** (待優化參數): 各個抽水井的抽水率
    * **目標函數**: 模擬水頭值與觀測水位之均方根誤差 (`Mean Square Error`)
    (*目的希望最小化目標函數，即最小化誤差*)
    * 天牛步長
    * 兩鬚間距

* 算法:
    1. 隨機初始化未知參數 (Pumping rate)
    2. 進行模擬
    3. 利用模擬水頭值與觀測水位計算 **目標函數** 
    4. 透過 `BAS` 調整參數，反覆疊代，直到目標函數小於閥值

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/168416976-8bc62e63-a839-44ba-9dec-d194c9b0ad56.png" widht=50%/>
</p>

---
### 研究區域

粗略說明：

* 研究區域位於台灣屏東。
* 下圖為觀測地下水位。

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640237-e52cecde-67de-4818-94fc-4c3c03219a4f.png" width=50%/>
</p>

---
### 地下水模擬

粗略說明：

1. 我們使用FEFLOW7.3建立我們的流動模型。
2. 設定邊界條件。（例如：Dirichlet、Neumann...）
3. 設定研究區域的水力傳導度和入流。
---
### 優化前

如下圖所示，在未設置井的情況下結果不好。（灰線：觀測；彩色線：模擬結果）

與觀測資料相比，以下為：

> **絕對誤差**: `6.87`
> **均方根誤差**: `7.83`
> **標準差**: `8`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640520-910c0a10-67a5-45de-b03b-93d0be45e868.png" width=200px/>
</p>

---
### 優化後
我們在研究區域內均勻設置了抽水井，然後使用了 `BAS` 算法。

> **絕對誤差**: `0.988`
> **均方根誤差**: `1.3`
> **標準差**: `1.3`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159641259-042c74c8-3028-4253-a7b8-249b46966bc5.png" width=60%/>
</p>

---
### 誤差分析比較

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178942962-eb72864d-f97b-45e6-b571-ab54cf841cc3.png" width=50% />

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178094741-34584c0d-b9a9-44c4-8386-3b2c3005522c.png" width=50%/>

<a href="#top">Back to top</a>
