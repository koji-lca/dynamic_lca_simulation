"""
generate_charts.py
ノートブック内の全グラフ + 追加図表を PNG として生成し
assets/charts/ に保存する
"""
import sys, os
from pathlib import Path

# src を path に追加
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np

try:
    import japanize_matplotlib          # 日本語フォント
except ImportError:
    pass

from dynamic_lca import (
    BernModel, Flow,
    crf_co2, crf_gas,
    dcf_co2, dcf_gas, dcf_re2020,
    dynamic_gwp, impulse_response_co2, impulse_response_gas, static_gwp,
)

# ── output dir ────────────────────────────────────────────────────────────────
CHARTS = Path(__file__).parent / "assets" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 140,
    "axes.unicode_minus": False,
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

BLUE   = "#2e86de"
ORANGE = "#e67e22"
GREEN  = "#27ae60"
RED    = "#c0392b"
PURPLE = "#8e44ad"
GRAY   = "#7f8c8d"
NAVY   = "#193950"
SUMPO  = "#0057BA"

HTI  = 100
STEP = 0.5
YRS  = list(range(0, HTI + 1))
MODEL = BernModel()


def save(fig, name):
    path = CHARTS / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=140)
    plt.close(fig)
    print(f"  ✅ {name}.png")
    return path


# ── Fig 01: Bernモデル・インパルス応答 ────────────────────────────────────────
def fig01_bern_impulse():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    y = [impulse_response_co2(t) for t in YRS]
    ax.plot(YRS, y, color=BLUE, lw=2.5, label="CO₂大気残存割合 r(t)")
    ax.fill_between(YRS, y, alpha=0.14, color=BLUE)
    ax.axhline(MODEL.c0, color=ORANGE, ls="--", lw=1.5,
               label=f"永続分率 a₀ = {MODEL.c0}")
    ax.set_xlabel("排出後の経過年数 [年]")
    ax.set_ylabel("大気残存割合")
    ax.set_title("IPCC AR4 Bern2.5CCモデル — CO₂インパルス応答 r(t)")
    ax.legend()
    ax.set_xlim(0, 100); ax.set_ylim(0, 1)
    fig.tight_layout()
    return save(fig, "fig01_bern_impulse")


# ── Fig 02: CRF/DCF 関係（3パネル、ノートブック Cell 4 相当）────────────────
def fig02_crf_dcf_relationship(t=50):
    elapsed = np.arange(0, HTI + STEP, STEP)
    rf_vals = [MODEL.radiative_efficiency * impulse_response_co2(u) for u in elapsed]
    num_dur = HTI - t
    num_x = elapsed[elapsed <= num_dur]
    num_y = [MODEL.radiative_efficiency * impulse_response_co2(u) for u in num_x]

    ref_crf = crf_co2(0, HTI, step_years=STEP)
    sel_crf = crf_co2(t, HTI, step_years=STEP)
    sel_dcf = dcf_co2(t, HTI, step_years=STEP)

    gases = [("CO2", BLUE), ("CH4", RED), ("N2O", PURPLE)]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: 積分範囲の可視化
    ax = axes[0]
    ax.plot(elapsed, rf_vals, color=BLUE, lw=2)
    ax.fill_between(elapsed, rf_vals, alpha=0.18, color=BLUE,
                    label=f"分母 CRF(0): 0〜{HTI}年")
    ax.fill_between(num_x, num_y, alpha=0.42, color=ORANGE,
                    label=f"分子 CRF(t): 0〜{num_dur}年")
    ax.axvline(num_dur, color=ORANGE, ls="--", lw=1.8)
    ax.set_title(f"CO₂の分母 vs 分子の積分範囲（t={t}年）")
    ax.set_xlabel("排出後の経過年 u"); ax.set_ylabel("放射強制力 RF(u)")
    ax.legend(fontsize=9)

    # Panel 2: CRF(t) ガス別
    ax = axes[1]
    for gas, color in gases:
        crf_vals = [crf_gas(yr, HTI, gas=gas, step_years=STEP) for yr in YRS]
        ax.plot(YRS, crf_vals, color=color, lw=2, label=gas)
        ax.scatter([t], [crf_gas(t, HTI, gas=gas, step_years=STEP)],
                   color=color, zorder=3, s=60)
    ax.axvline(t, color=ORANGE, ls="--", lw=1.8, label=f"t={t}年")
    ax.set_title("CRF(t): ガス別の累積放射強制力")
    ax.set_xlabel("発生年 t"); ax.set_ylabel("CRF")
    ax.legend()

    # Panel 3: DCF(t) ガス別
    ax = axes[2]
    for gas, color in gases:
        dcf_vals = [dcf_gas(yr, HTI, gas=gas, step_years=STEP) for yr in YRS]
        ax.plot(YRS, dcf_vals, color=color, lw=2, label=gas)
        ax.scatter([t], [dcf_gas(t, HTI, gas=gas, step_years=STEP)],
                   color=color, zorder=3, s=60)
    ax.axvline(t, color=ORANGE, ls="--", lw=1.8, label=f"t={t}年")
    ax.set_title("DCF(t) = 分子CRF / 分母CRF")
    ax.set_xlabel("発生年 t"); ax.set_ylabel("DCF"); ax.set_ylim(0, 1.05)
    ax.legend()

    fig.suptitle(
        f"CRF/DCFの関係（HTI={HTI}年） — "
        f"CO₂: CRF(0)={ref_crf:.3e}, CRF({t})={sel_crf:.3e}, DCF({t})={sel_dcf:.3f}",
        fontsize=11)
    fig.tight_layout()
    return save(fig, "fig02_crf_dcf_relationship")


# ── Fig 03: DCF(t) Bern vs RE2020 精度比較 ──────────────────────────────────
def fig03_dcf_re2020_vs_bern():
    bern_vals  = [dcf_co2(t, HTI, step_years=STEP) for t in YRS]
    re20_vals  = [dcf_re2020(t) for t in YRS]
    # t=0..50のみ誤差計算（t>50はRE2020が上限0.58固定でbernと比較困難）
    error_yrs  = [t for t in YRS if t <= 50]
    error_pct  = [(dcf_re2020(t) - dcf_co2(t, HTI, step_years=STEP)) /
                  dcf_co2(t, HTI, step_years=STEP) * 100
                  for t in error_yrs]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.plot(YRS, bern_vals, color=BLUE, lw=2.5, label="Bern2.5CC（非線形DCF）")
    ax1.plot(YRS, re20_vals, color=ORANGE, lw=2, ls="--",
             label="RE2020線形近似: 1−0.00842×t")
    ax1.axhline(0.58, color=RED, lw=1, ls=":", alpha=0.7, label="下限 0.580（t≥50）")
    for yr, label in [(25, "t=25"), (50, "t=50")]:
        b = dcf_co2(yr, HTI, step_years=STEP)
        r = dcf_re2020(yr)
        ax1.annotate(f"Bern={b:.3f}\nRE2020={r:.3f}",
                     (yr, b), xytext=(yr+3, b+0.05),
                     fontsize=8.5, color=NAVY,
                     arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))
    ax1.set_xlabel("発生年 t [年]"); ax1.set_ylabel("DCF(t)")
    ax1.set_title("DCF(t): Bern非線形 vs RE2020線形近似")
    ax1.set_xlim(0, 100); ax1.set_ylim(0.5, 1.05)
    ax1.legend()

    ax2.plot(error_yrs, error_pct, color=PURPLE, lw=2)
    ax2.fill_between(error_yrs, error_pct, alpha=0.15, color=PURPLE)
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_xlabel("発生年 t [年]"); ax2.set_ylabel("誤差 [%]")
    ax2.set_title("RE2020の近似誤差 = (RE2020 − Bern) / Bern × 100")
    ax2.set_xlim(0, 50)
    for yr in [25, 50]:
        e = error_pct[error_yrs.index(yr)]
        ax2.annotate(f"t={yr}年\n{e:+.1f}%", (yr, e), xytext=(yr-10, e+0.5),
                     fontsize=9, arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))

    fig.suptitle("RE2020線形近似の精度: Bern2.5CC非線形DCFとの比較（HTI=100年）")
    fig.tight_layout()
    return save(fig, "fig03_dcf_re2020_vs_bern")


# ── Fig 04: 木材ケース GWP比較棒グラフ（ノートブック Cell 7 相当）────────────
def fig04_wood_gwp_comparison():
    dos = [25, 50, 75, 100]
    scenarios = {
        "固定+放出（−1/+1）": lambda do: [
            Flow(year=0,  amount=-100, name="固定"), Flow(year=do, amount=100, name="放出")],
        "放出のみ": lambda do: [Flow(year=do, amount=100, name="放出")],
        "固定のみ":  lambda do: [Flow(year=0,  amount=-100, name="固定")],
    }
    methods = [
        ("静的GWP",         GRAY,   lambda fl, do: static_gwp(fl)),
        ("動的GWP（Bern）",  BLUE,   lambda fl, do: dynamic_gwp(fl, method="bern",   horizon_years=HTI, step_years=STEP)),
        ("動的GWP（RE2020）",GREEN,  lambda fl, do: dynamic_gwp(fl, method="re2020")),
    ]

    fig, axes = plt.subplots(1, len(dos), figsize=(16, 5), sharey=True)
    for ax, do in zip(axes, dos):
        sc_names = list(scenarios.keys())
        x = np.arange(len(sc_names))
        w = 0.25
        for i, (method_name, color, fn) in enumerate(methods):
            vals = [fn(scenarios[sc](do), do) for sc in sc_names]
            bars = ax.bar(x + (i - 1) * w, vals, width=w, label=method_name,
                          color=color, alpha=0.88)
            for bar, v in zip(bars, vals):
                if abs(v) > 1:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (2 if v >= 0 else -8),
                            f"{v:.0f}", ha="center", fontsize=7.5)
        ax.axhline(0, color="black", lw=0.8)
        ax.set_title(f"DO = {do}年")
        ax.set_xticks(x); ax.set_xticklabels(sc_names, fontsize=8.5)
        ax.set_ylabel("kgCO₂eq" if do == dos[0] else "")
    axes[0].legend(loc="lower left", fontsize=9)
    fig.suptitle("木材バイオジェニック炭素の GWP比較（評価前提別・DO別）", fontsize=12)
    fig.tight_layout()
    return save(fig, "fig04_wood_gwp_comparison")


# ── Fig 05: Bern感度 2×2（ノートブック Cell 7 相当）────────────────────────
def fig05_bern_sensitivity(t=50, do=50):
    response_vals = [impulse_response_co2(yr) for yr in YRS]
    crf_vals      = [crf_co2(yr, HTI, step_years=STEP) for yr in YRS]
    dcf_bern_vals = [dcf_co2(yr, HTI, step_years=STEP) for yr in YRS]
    dcf_re20_vals = [dcf_re2020(yr) for yr in YRS]
    ref_crf = crf_co2(0, HTI, step_years=STEP)

    scenarios = {
        "固定+放出": [Flow(year=0, amount=-100, name="固定", category="A1-A3"),
                     Flow(year=do, amount=100, name="放出", category="C")],
        "放出のみ":  [Flow(year=do, amount=100, name="放出", category="C")],
        "固定のみ":  [Flow(year=0, amount=-100, name="固定", category="A1-A3")],
    }
    results = {k: {
        "静的GWP": static_gwp(v),
        "動的（Bern）": dynamic_gwp(v, method="bern", horizon_years=HTI, step_years=STEP),
        "動的（RE2020）": dynamic_gwp(v, method="re2020"),
    } for k, v in scenarios.items()}

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    axes[0,0].plot(YRS, response_vals, color=PURPLE, lw=2)
    axes[0,0].fill_between(YRS, response_vals, color=PURPLE, alpha=0.14)
    axes[0,0].axhline(MODEL.c0, color=ORANGE, ls="--", lw=1.5,
                      label=f"永続分率 a₀={MODEL.c0}")
    axes[0,0].set_title("Bernインパルス応答 r(t)")
    axes[0,0].set_xlabel("経過年"); axes[0,0].set_ylabel("大気残存割合")
    axes[0,0].legend()

    axes[0,1].plot(YRS, crf_vals, color=BLUE, lw=2)
    axes[0,1].fill_between(YRS, crf_vals, color=BLUE, alpha=0.14)
    axes[0,1].axhline(ref_crf, color=BLUE, ls=":", lw=1.5, label="分母 CRF(0)")
    axes[0,1].axvline(t, color=ORANGE, ls="--", lw=1.8, label=f"t={t}年")
    axes[0,1].set_title("CRF(t): 発生年に応じた積分値")
    axes[0,1].set_xlabel("発生年 t"); axes[0,1].set_ylabel("CRF")
    axes[0,1].legend()

    axes[1,0].plot(YRS, dcf_bern_vals, color=GREEN, lw=2.5, label="Bern DCF（非線形）")
    axes[1,0].fill_between(YRS, dcf_bern_vals, color=GREEN, alpha=0.12)
    axes[1,0].plot(YRS, dcf_re20_vals, color=GRAY, lw=2, ls="--", label="RE2020近似")
    axes[1,0].axvline(t,  color=ORANGE, ls="--", lw=1.8, label=f"t={t}年")
    axes[1,0].axvline(do, color=RED,    ls=":",  lw=1.5, label=f"DO={do}年")
    bern_at_do = dcf_co2(do, HTI, step_years=STEP)
    re20_at_do = dcf_re2020(do)
    axes[1,0].annotate(f"Bern DCF({do})={bern_at_do:.3f}\nRE2020={re20_at_do:.3f}",
                       (do, bern_at_do), xytext=(do+5, bern_at_do+0.08),
                       fontsize=9, arrowprops=dict(arrowstyle="->", color=NAVY))
    axes[1,0].set_title("DCF(t): Bern vs RE2020線形近似")
    axes[1,0].set_xlabel("発生年 t"); axes[1,0].set_ylabel("DCF"); axes[1,0].set_ylim(0, 1.05)
    axes[1,0].legend()

    sc_names = list(results.keys())
    x = np.arange(len(sc_names)); w = 0.25
    for i, (method, color) in enumerate([("静的GWP",GRAY),("動的（Bern）",BLUE),("動的（RE2020）",GREEN)]):
        vals = [results[sc][method] for sc in sc_names]
        axes[1,1].bar(x + (i-1)*w, vals, width=w, label=method, color=color, alpha=0.88)
    axes[1,1].axhline(0, color="black", lw=0.8)
    axes[1,1].set_title(f"木材ケース GWP比較（DO={do}年）")
    axes[1,1].set_ylabel("kgCO₂eq")
    axes[1,1].set_xticks(x); axes[1,1].set_xticklabels(sc_names)
    axes[1,1].legend()

    fig.suptitle(
        f"Bern感度シミュレーション (HTI={HTI}年, t={t}年, DO={do}年) — "
        f"DCF({t})={dcf_bern_vals[t]:.3f}, DCF({do})={bern_at_do:.3f}", fontsize=11)
    fig.tight_layout()
    return save(fig, "fig05_bern_sensitivity")


# ── Fig 06: CO2/CH4/N2O DCF比較 ─────────────────────────────────────────────
def fig06_gas_dcf_comparison():
    gases = [("CO2", BLUE, "実線"), ("CH4", RED, "破線"), ("N2O", PURPLE, "点線")]
    ls_map = {"実線": "-", "破線": "--", "点線": ":"}

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for gas, color, lstyle in gases:
        dcf_vals = [dcf_gas(t, HTI, gas=gas, step_years=STEP) for t in YRS]
        axes[0].plot(YRS, dcf_vals, color=color, lw=2.5,
                     ls=ls_map[lstyle], label=gas)
    axes[0].axvline(50, color=ORANGE, ls="--", lw=1.5, label="t=50年（RE2020解体段階）")
    axes[0].set_title("DCF(t): CO₂・CH₄・N₂O 比較（HTI=100年）")
    axes[0].set_xlabel("発生年 t [年]"); axes[0].set_ylabel("DCF(t)")
    axes[0].set_ylim(0, 1.05); axes[0].legend()

    key_years = [0, 10, 25, 50, 75, 100]
    data = {gas: [dcf_gas(t, HTI, gas=gas, step_years=STEP) for t in key_years]
            for gas, _, _ in gases}
    x = np.arange(len(key_years)); w = 0.27
    for i, (gas, color, _) in enumerate(gases):
        axes[1].bar(x + (i-1)*w, data[gas], width=w, label=gas, color=color, alpha=0.85)
        for j, (xi, v) in enumerate(zip(x, data[gas])):
            axes[1].text(xi + (i-1)*w, v + 0.01, f"{v:.2f}",
                         ha="center", fontsize=7.5, rotation=90)
    axes[1].set_title("主要年のDCF値: CO₂・CH₄・N₂O")
    axes[1].set_xlabel("発生年 t [年]"); axes[1].set_ylabel("DCF(t)")
    axes[1].set_xticks(x); axes[1].set_xticklabels([f"{t}年" for t in key_years])
    axes[1].set_ylim(0, 1.15); axes[1].legend()

    fig.suptitle("ガス種別DCF(t): 将来排出が気候影響を割引される程度の比較")
    fig.tight_layout()
    return save(fig, "fig06_gas_dcf_comparison")


# ── Fig 07: RE2020モジュール別DCF値と Ic算定への影響 ────────────────────────
def fig07_module_dcf_impact():
    modules = ["A1-A3\n(t=0)", "B段階\n(t=25)", "C段階\n(t=50)"]
    years   = [0, 25, 50]
    dcf_bern = [dcf_co2(t, HTI, step_years=STEP) for t in years]
    dcf_re20 = [dcf_re2020(t) for t in years]

    # CLT vs コンクリートの排出量（代表値）
    # CLT: A1-A3=-270(biogenic fix), C4=+270(biogenic release), 化石=+80
    # RC:  A1-A3=+300(化石), B=+50, C=+50
    clt_ghg  = [-270, 0, 270]   # バイオジェニック炭素のみで単純化
    rc_ghg   = [ 300, 50,  50]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: DCF比較
    x = np.arange(len(modules)); w = 0.35
    axes[0].bar(x - w/2, dcf_bern, width=w, color=BLUE,   label="Bern DCF",  alpha=0.85)
    axes[0].bar(x + w/2, dcf_re20, width=w, color=ORANGE, label="RE2020近似", alpha=0.85)
    for xi, b, r in zip(x, dcf_bern, dcf_re20):
        axes[0].text(xi - w/2, b + 0.01, f"{b:.3f}", ha="center", fontsize=10, fontweight="bold")
        axes[0].text(xi + w/2, r + 0.01, f"{r:.3f}", ha="center", fontsize=10)
    axes[0].set_title("モジュール別 DCF値（HTI=100年）")
    axes[0].set_xticks(x); axes[0].set_xticklabels(modules)
    axes[0].set_ylabel("DCF"); axes[0].set_ylim(0, 1.15); axes[0].legend()

    # Panel 2: CLTの静的 vs 動的評価
    clt_static  = [g * 1.0       for g in clt_ghg]
    clt_dynamic = [g * dcf_re20[i] for i, g in enumerate(clt_ghg)]
    x2 = np.arange(len(modules)); w2 = 0.35
    bars_s = axes[1].bar(x2 - w2/2, clt_static,  width=w2, color=GRAY,  label="静的LCA", alpha=0.85)
    bars_d = axes[1].bar(x2 + w2/2, clt_dynamic, width=w2, color=GREEN, label="動的LCA（RE2020）", alpha=0.85)
    axes[1].axhline(0, color="black", lw=0.8)
    net_s = sum(clt_static);  net_d = sum(clt_dynamic)
    axes[1].annotate(f"正味: {net_s:+.0f} kgCO₂eq", xy=(2.5, net_s*0.6),
                     fontsize=9, color=GRAY, ha="right")
    axes[1].annotate(f"正味: {net_d:+.0f} kgCO₂eq", xy=(2.5, net_d*1.4),
                     fontsize=9, color=GREEN, ha="right")
    axes[1].set_title("CLT（木材）: 静的 vs 動的LCA")
    axes[1].set_xticks(x2); axes[1].set_xticklabels(modules)
    axes[1].set_ylabel("GHG排出量 [kgCO₂eq]"); axes[1].legend()

    # Panel 3: 静的/動的の正味比較
    buildings = ["CLT構造", "RC造コンクリート"]
    static_net  = [sum(clt_ghg),  sum(rc_ghg)]
    dynamic_net = [sum(g * dcf_re20[i] for i,g in enumerate(clt_ghg)),
                   sum(g * dcf_re20[i] for i,g in enumerate(rc_ghg))]
    xb = np.arange(2); wb = 0.35
    b1 = axes[2].bar(xb - wb/2, static_net,  width=wb, color=GRAY,  label="静的LCA", alpha=0.85)
    b2 = axes[2].bar(xb + wb/2, dynamic_net, width=wb, color=GREEN, label="動的LCA（RE2020）", alpha=0.85)
    axes[2].axhline(0, color="black", lw=0.8)
    for b, v in list(zip(b1, static_net)) + list(zip(b2, dynamic_net)):
        axes[2].text(b.get_x()+b.get_width()/2,
                     v + (5 if v >= 0 else -15), f"{v:+.0f}",
                     ha="center", fontsize=10, fontweight="bold")
    axes[2].set_title("静的 vs 動的LCA — 建材別の正味評価")
    axes[2].set_xticks(xb); axes[2].set_xticklabels(buildings)
    axes[2].set_ylabel("正味GHG [kgCO₂eq]"); axes[2].legend()

    fig.suptitle("RE2020のDCF係数: モジュール別影響とCLT vs RC造の評価逆転")
    fig.tight_layout()
    return save(fig, "fig07_module_dcf_impact")


# ── Fig 08: RE2020 seuil値タイムライン ──────────────────────────────────────
def fig08_seuil_timeline():
    phases = ["Phase 1\n2022-2024", "Phase 2\n2025-2027",
              "Phase 3\n2028-2030\n（予定）", "Phase 4\n2031-\n（目標）"]
    seuil = [640, 530, 490, 350]
    colors_bar = [SUMPO, "#1a73c7", "#1558a0", NAVY]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    bars = ax1.bar(phases, seuil, color=colors_bar, alpha=0.88, width=0.6)
    ax1.axhline(640, color=GRAY, ls=":", lw=1.2, alpha=0.6)
    for bar, v in zip(bars, seuil):
        ax1.text(bar.get_x()+bar.get_width()/2, v + 6,
                 f"{v}\nkgCO₂eq/m²",
                 ha="center", va="bottom", fontsize=10, fontweight="bold", color="white",
                 bbox=dict(facecolor=NAVY, alpha=0.7, pad=3, edgecolor="none"))
    reductions = [0, (640-530)/640*100, (640-490)/640*100, (640-350)/640*100]
    for i, (bar, r) in enumerate(zip(bars, reductions)):
        if r > 0:
            ax1.text(bar.get_x()+bar.get_width()/2, 30,
                     f"−{r:.0f}%",
                     ha="center", fontsize=9, color="white", fontweight="bold")
    ax1.set_title("Ic_construction seuil値の段階的引き下げ\n（住宅集合住宅）")
    ax1.set_ylabel("seuil値 [kgCO₂eq/m²]"); ax1.set_ylim(0, 750)
    ax1.grid(axis="y", alpha=0.3)

    # Panel 2: 達成のための炭素削減イメージ
    categories = ["A1-A3\n建材製造", "B段階\n使用・修繕", "C段階\n解体・廃棄", "StockC\n木材炭素貯蔵"]
    base_vals   = [450,  80,  110, 0]
    target_vals = [250,  50,   50, -150]  # Phase 4目標のイメージ
    x = np.arange(len(categories)); w = 0.35
    ax2.bar(x - w/2, base_vals,   width=w, color=GRAY,    label="Phase 1水準（現状）", alpha=0.85)
    ax2.bar(x + w/2, target_vals, width=w, color=GREEN,   label="Phase 4目標水準", alpha=0.85)
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_title("Ic_construction 内訳（Phase 1 vs Phase 4目標）\n※イメージ値")
    ax2.set_xticks(x); ax2.set_xticklabels(categories)
    ax2.set_ylabel("kgCO₂eq/m²"); ax2.legend()
    for xi, (b, t_) in enumerate(zip(base_vals, target_vals)):
        ax2.text(xi-w/2, b+5, f"{b:+}", ha="center", fontsize=9)
        ax2.text(xi+w/2, t_+(5 if t_ >= 0 else -18), f"{t_:+}", ha="center", fontsize=9, fontweight="bold")

    fig.suptitle("RE2020 段階的seuil値と炭素削減目標（Ic_construction）")
    fig.tight_layout()
    return save(fig, "fig08_seuil_timeline")


# ── Fig 09: 時間地平の科学的比較（政策的均衡点）────────────────────────────
def fig09_time_horizon_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    horizons = [20, 50, 100, 200, 500]
    colors_h = [RED, ORANGE, BLUE, GREEN, PURPLE]
    for h, c in zip(horizons, colors_h):
        if h <= 200:
            yrs = list(range(0, h+1))
            dcf_vals = [dcf_co2(t, h, step_years=0.5) for t in yrs]
            axes[0].plot(yrs, dcf_vals, color=c, lw=2, label=f"HTI={h}年")
    axes[0].set_title("時間地平（HTI）別のDCF(t)曲線")
    axes[0].set_xlabel("発生年 t [年]"); axes[0].set_ylabel("DCF(t)")
    axes[0].set_ylim(0, 1.05); axes[0].legend()

    t50_dcf = {h: dcf_co2(50, h, step_years=0.5) for h in horizons if h >= 50}
    ax2 = axes[1]
    bars = ax2.bar([str(h) for h in t50_dcf.keys()],
                   list(t50_dcf.values()), color=SUMPO, alpha=0.85)
    ax2.axhline(0.58, color=RED, ls="--", lw=1.5, label="RE2020固定値 0.580")
    for bar, v in zip(bars, t50_dcf.values()):
        ax2.text(bar.get_x()+bar.get_width()/2, v + 0.01,
                 f"{v:.3f}", ha="center", fontsize=11, fontweight="bold")
    ax2.set_title("解体段階（t=50年）のDCF値: HTIによる違い")
    ax2.set_xlabel("時間地平 HTI [年]"); ax2.set_ylabel("DCF(t=50年)")
    ax2.set_ylim(0, 1.0); ax2.legend()

    fig.suptitle("時間地平（HTI）の選択がDCF評価に与える影響: 政治的均衡点としての100年")
    fig.tight_layout()
    return save(fig, "fig09_time_horizon_comparison")


# ── Fig 10: バイオジェニック炭素サイクル（フロー図）────────────────────────
def fig10_biogenic_carbon_cycle():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    def box(x, y, w, h, text, fc, ec=NAVY, fontsize=10, bold=False):
        rect = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
                                       boxstyle="round,pad=0.1",
                                       facecolor=fc, edgecolor=ec, lw=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fontsize, fontweight="bold" if bold else "normal",
                color="white" if fc in (NAVY, SUMPO, RED) else NAVY,
                wrap=True, multialignment="center")

    def arrow(x1, y1, x2, y2, label="", color=NAVY):
        ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.15, my, label, fontsize=8.5, color=color)

    # Nodes
    box(5, 5.3, 2.5, 0.7, "大気中CO₂", NAVY, bold=True)
    box(5, 3.8, 2.5, 0.7, "樹木バイオマス（生体）", "#2980b9", bold=True)
    box(5, 2.4, 2.5, 0.7, "製材・CLT\n（製品内貯蔵）", SUMPO, bold=True)
    box(5, 0.9, 2.5, 0.7, "建物構造材\n（50年以上貯蔵）", "#1a8a3a", bold=True)
    # Disposal routes
    box(2, -0.3, 1.8, 0.65, "焼却（C4）\nCO₂即時放出", RED)
    box(5, -0.3, 1.8, 0.65, "埋立（C4）\nCH₄+CO₂徐放", ORANGE)
    box(8, -0.3, 1.8, 0.65, "再利用（D）\n貯蔵延長", GREEN)

    # Arrows
    arrow(5, 4.95, 5, 4.15, "  光合成（NPP）", "#2980b9")
    arrow(5, 3.45, 5, 2.75, "  伐採・搬出", SUMPO)
    arrow(5, 2.05, 5, 1.25, "  建設（A1-A3）\n  DCF=1.0", "#1a8a3a")
    arrow(4.2, 0.57, 2.5, 0.05, "", RED)
    arrow(5,   0.57, 5,   0.05, "", ORANGE)
    arrow(5.8, 0.57, 7.5, 0.05, "", GREEN)
    # Return arrows
    ax.annotate("", xy=(4.0, 5.0), xytext=(1.8, -0.05),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5,
                                connectionstyle="arc3,rad=0.35"))
    ax.text(1.0, 2.5, "RE2020\nDCF(50)=0.58", fontsize=8.5, color=RED,
            ha="center", fontweight="bold")

    # DCF labels
    ax.text(7.0, 2.4, "A1-A3: DCF=1.000\n建設時に固定\n→ StockCクレジット",
            fontsize=8, color="#1a8a3a",
            bbox=dict(facecolor="#e8f5e9", edgecolor="#1a8a3a", pad=4))
    ax.text(7.0, 0.7, "C4: DCF=0.580\n解体時に放出\n→ 42%割引計上",
            fontsize=8, color=RED,
            bbox=dict(facecolor="#fdecea", edgecolor=RED, pad=4))

    ax.set_title("木材バイオジェニック炭素サイクルと RE2020 DCF適用箇所",
                 fontsize=13, fontweight="bold", color=NAVY, pad=10)
    fig.tight_layout()
    return save(fig, "fig10_biogenic_carbon_cycle")


# ── Fig 11: AR4 vs AR6 パラメータ比較 ────────────────────────────────────────
def fig11_ar4_vs_ar6():
    ar4 = BernModel(c0=0.217, c1=0.259, tau1=172.9, c2=0.338, tau2=18.51, c3=0.186, tau3=1.186)
    ar6 = BernModel(c0=0.200, c1=0.335, tau1=394.4, c2=0.376, tau2=36.54, c3=0.089, tau3=4.304)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    yr_long = list(range(0, 201))
    ir_ar4 = [impulse_response_co2(t, model=ar4) for t in yr_long]
    ir_ar6 = [impulse_response_co2(t, model=ar6) for t in yr_long]
    axes[0].plot(yr_long, ir_ar4, color=BLUE,   lw=2.5, label=f"AR4 (a₀={ar4.c0})")
    axes[0].plot(yr_long, ir_ar6, color=ORANGE, lw=2.5, ls="--", label=f"AR6 (a₀={ar6.c0})")
    axes[0].set_title("CO₂インパルス応答: AR4 vs AR6")
    axes[0].set_xlabel("経過年 [年]"); axes[0].set_ylabel("大気残存割合")
    axes[0].legend()

    dcf_ar4  = [dcf_co2(t, HTI, step_years=STEP, model=ar4) for t in YRS]
    dcf_ar6  = [dcf_co2(t, HTI, step_years=STEP, model=ar6) for t in YRS]
    dcf_re20 = [dcf_re2020(t) for t in YRS]
    axes[1].plot(YRS, dcf_ar4,  color=BLUE,   lw=2.5, label="Bern AR4")
    axes[1].plot(YRS, dcf_ar6,  color=ORANGE, lw=2.5, ls="--", label="Bern AR6（推奨値）")
    axes[1].plot(YRS, dcf_re20, color=GRAY,   lw=2,   ls=":",  label="RE2020線形近似")
    axes[1].set_title("DCF(t): AR4 vs AR6 vs RE2020（HTI=100年）")
    axes[1].set_xlabel("発生年 t [年]"); axes[1].set_ylabel("DCF(t)")
    axes[1].set_ylim(0.5, 1.05); axes[1].legend()

    key_t = [0, 10, 25, 50]
    ar4_vals  = [dcf_co2(t, HTI, step_years=STEP, model=ar4) for t in key_t]
    ar6_vals  = [dcf_co2(t, HTI, step_years=STEP, model=ar6) for t in key_t]
    re20_vals = [dcf_re2020(t) for t in key_t]
    x = np.arange(len(key_t)); w = 0.27
    axes[2].bar(x - w, ar4_vals,  width=w, color=BLUE,   label="AR4",  alpha=0.85)
    axes[2].bar(x,     ar6_vals,  width=w, color=ORANGE, label="AR6",  alpha=0.85)
    axes[2].bar(x + w, re20_vals, width=w, color=GRAY,   label="RE2020", alpha=0.85)
    axes[2].set_title("主要時点のDCF値: AR4 vs AR6 vs RE2020")
    axes[2].set_xticks(x); axes[2].set_xticklabels([f"t={t}" for t in key_t])
    axes[2].set_ylabel("DCF"); axes[2].set_ylim(0.5, 1.1); axes[2].legend()
    for xi, (a4, a6, r) in enumerate(zip(ar4_vals, ar6_vals, re20_vals)):
        for xoff, v, c in [(-w, a4, BLUE), (0, a6, ORANGE), (w, r, GRAY)]:
            axes[2].text(xi+xoff, v+0.003, f"{v:.3f}", ha="center", fontsize=7.5,
                         color=c, fontweight="bold")

    fig.suptitle("IPCC AR4 vs AR6 Bernモデルパラメータ更新が DCFに与える影響")
    fig.tight_layout()
    return save(fig, "fig11_ar4_vs_ar6")


# ── Fig 12: 動的LCA 導入タイムライン（年表）────────────────────────────────
def fig12_policy_timeline():
    events = [
        (2007, "グルネル環境RTT\n炭素評価を政策課題化", BLUE),
        (2009, "Benoist博士論文\n線形近似1-0.00842t導出", BLUE),
        (2010, "Levasseur et al.\n動的LCA基礎論文", GREEN),
        (2016, "E+C-実証プログラム開始\n2,200棟実証", ORANGE),
        (2018, "Solinnen報告書\nElodie v2.5実装", ORANGE),
        (2019, "EUグリーンディール\nWLC義務化の文脈確立", PURPLE),
        (2021, "RE2020法令公布\nDécret 2021-1004", RED),
        (2022, "RE2020施行\nEU議長国として発信", RED),
        (2025, "ISO 21391-1:2025\n仏AFNOR主導策定完了", NAVY),
        (2028, "Phase 3予定\nISO 21391-1移行検討", GRAY),
    ]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(2005, 2030); ax.set_ylim(-1.5, 2.5)
    ax.axis("off")

    ax.axhline(0, color=NAVY, lw=2.5, alpha=0.8)
    for i, (year, label, color) in enumerate(events):
        y = 0.9 if i % 2 == 0 else -0.9
        ax.plot([year, year], [0, y*0.85], color=color, lw=1.8, alpha=0.8)
        ax.scatter([year], [0], color=color, s=80, zorder=5)
        ax.text(year, y + (0.15 if y > 0 else -0.15), label,
                ha="center", va="bottom" if y > 0 else "top",
                fontsize=8, color=NAVY,
                bbox=dict(facecolor="white", edgecolor=color, pad=3, lw=1.5),
                multialignment="center")
        ax.text(year, 0.05, str(year), ha="center", va="bottom",
                fontsize=7.5, color=color, fontweight="bold")

    ax.set_title("動的LCA制度化の主要マイルストーン（2007-2028年）",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.95)
    fig.tight_layout()
    return save(fig, "fig12_policy_timeline")


# ── メイン ──────────────────────────────────────────────────────────────────
def main():
    print("📊 グラフ生成開始 →", CHARTS)
    paths = {}
    funcs = [
        ("fig01", fig01_bern_impulse),
        ("fig02", fig02_crf_dcf_relationship),
        ("fig03", fig03_dcf_re2020_vs_bern),
        ("fig04", fig04_wood_gwp_comparison),
        ("fig05", fig05_bern_sensitivity),
        ("fig06", fig06_gas_dcf_comparison),
        ("fig07", fig07_module_dcf_impact),
        ("fig08", fig08_seuil_timeline),
        ("fig09", fig09_time_horizon_comparison),
        ("fig10", fig10_biogenic_carbon_cycle),
        ("fig11", fig11_ar4_vs_ar6),
        ("fig12", fig12_policy_timeline),
    ]
    for key, fn in funcs:
        try:
            paths[key] = fn()
        except Exception as e:
            print(f"  ⚠ {key} 失敗: {e}")
    print(f"\n🎉 {len(paths)} / {len(funcs)} 枚生成完了")
    return paths

if __name__ == "__main__":
    main()
