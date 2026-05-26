from dynamic_lca import Flow, dcf_co2, dcf_re2020, dynamic_gwp, static_gwp


flows = [
    Flow(year=0, amount=-100, name="biogenic carbon uptake", category="A1-A3"),
    Flow(year=50, amount=100, name="end-of-life release", category="C"),
]

print("DCF Bern CO2, t=50:", round(dcf_co2(50), 3))
print("DCF RE2020, t=50:", round(dcf_re2020(50), 3))
print("Static GWP:", round(static_gwp(flows), 3))
print("Dynamic GWP Bern:", round(dynamic_gwp(flows, method="bern"), 3))
print("Dynamic GWP RE2020:", round(dynamic_gwp(flows, method="re2020"), 3))
