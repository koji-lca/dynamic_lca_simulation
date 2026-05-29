# Dynamic LCA Simulation

Levasseur et al. による動的LCAの考え方に基づき、CO₂・CH₄・N₂Oの動的特性化係数（DCF）と静的/動的GWPを計算するためのPythonライブラリです。

## 機能

- IPCC AR4 Bern2.5CCモデルによるCO₂インパルス応答 `r(t)`
- CH₄・N₂Oの一次減衰モデルによるインパルス応答
- 累積放射強制力（CRF）の数値積分
- Levasseur型のDCF計算
- RE2020線形近似DCF
- 排出・吸収フローからの静的GWP/動的GWP集計

## インストール

```bash
python3 -m pip install -e .
```

開発用テストを実行する場合は次を使います。

```bash
python3 -m pip install -e '.[dev]'
python3 -m pytest
```

## 可視化Notebook

計算結果をグラフで確認する場合は、開発用依存をインストールしたうえでJupyter Notebookを起動します。

```bash
python3 -m pip install -e '.[dev]'
python3 -m jupyter notebook notebooks/dynamic_lca_visualization.ipynb
```

Notebookでは `japanize-matplotlib` を使っているため、グラフの日本語タイトル・軸ラベル・凡例が文字化けしにくくなっています。

## 基本例

```python
from dynamic_lca import Flow, dynamic_gwp, static_gwp

flows = [
    Flow(year=0, amount=-100, name="biogenic carbon uptake"),
    Flow(year=50, amount=100, name="end-of-life release"),
]

print(static_gwp(flows))
print(dynamic_gwp(flows, method="bern"))
print(dynamic_gwp(flows, method="re2020"))
```

`amount` は排出を正、吸収を負として入力します。`gwp` は各フローに掛けるGWP係数で、CO₂の場合は既定値の `1.0` を使います。

## 主要API

- `impulse_response_co2(t)`
- `impulse_response_gas(t, gas="CO2")`
- `crf_co2(start_year, horizon_years=100)`
- `crf_gas(start_year, horizon_years=100, gas="CO2")`
- `dcf_co2(year, horizon_years=100)`
- `dcf_gas(year, horizon_years=100, gas="CO2")`
- `dcf_re2020(year)`
- `Flow(year, amount, gwp=1.0, name=None, category=None)`
- `static_gwp(flows)`
- `dynamic_gwp(flows, method="bern", horizon_years=100)`

## 仕様上の前提

- Bern2.5CCの係数は報告書第4章に記載された値を使います。
- CH₄・N₂Oは代表的な大気寿命と放射効率を使った簡略な一次減衰モデルです。
- RE2020近似は `0 <= t <= 50` で `1 - 0.00842 * t`、`t > 50` で `0.580` とします。
- ISO 21391-1:2025の詳細実装、外部LCAデータベース連携は未実装です。
