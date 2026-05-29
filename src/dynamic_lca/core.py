from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Literal


@dataclass(frozen=True)
class BernModel:
    c0: float = 0.217
    c1: float = 0.259
    c2: float = 0.338
    c3: float = 0.186
    tau1: float = 172.9
    tau2: float = 18.51
    tau3: float = 1.186
    radiative_efficiency: float = 1.55e-15

    def impulse_response(self, time_years: float) -> float:
        _validate_non_negative_finite(time_years, "time_years")
        return (
            self.c0
            + self.c1 * math.exp(-time_years / self.tau1)
            + self.c2 * math.exp(-time_years / self.tau2)
            + self.c3 * math.exp(-time_years / self.tau3)
        )


@dataclass(frozen=True)
class GasModel:
    name: str
    lifetime_years: float
    radiative_efficiency: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.lifetime_years) or self.lifetime_years <= 0:
            raise ValueError("lifetime_years must be positive")
        if not math.isfinite(self.radiative_efficiency) or self.radiative_efficiency <= 0:
            raise ValueError("radiative_efficiency must be positive")

    def impulse_response(self, time_years: float) -> float:
        _validate_non_negative_finite(time_years, "time_years")
        return math.exp(-time_years / self.lifetime_years)


@dataclass(frozen=True)
class Flow:
    year: float
    amount: float
    gwp: float = 1.0
    name: str | None = None
    category: str | None = None

    def __post_init__(self) -> None:
        _validate_non_negative_finite(self.year, "year")
        _validate_finite(self.amount, "amount")
        _validate_finite(self.gwp, "gwp")


DEFAULT_BERN_MODEL = BernModel()
DEFAULT_CH4_MODEL = GasModel(name="CH4", lifetime_years=12.4, radiative_efficiency=1.28e-13)
DEFAULT_N2O_MODEL = GasModel(name="N2O", lifetime_years=121.0, radiative_efficiency=3.03e-13)
DEFAULT_GAS_MODELS = {
    "CO2": DEFAULT_BERN_MODEL,
    "CH4": DEFAULT_CH4_MODEL,
    "N2O": DEFAULT_N2O_MODEL,
}
DynamicMethod = Literal["bern", "re2020"]
GasName = Literal["CO2", "CH4", "N2O"]


def impulse_response_co2(time_years: float, model: BernModel = DEFAULT_BERN_MODEL) -> float:
    return model.impulse_response(time_years)


def impulse_response_gas(
    time_years: float,
    gas: GasName = "CO2",
    *,
    model: BernModel | GasModel | None = None,
) -> float:
    selected_model = _resolve_gas_model(gas, model)
    return selected_model.impulse_response(time_years)


def crf_co2(
    start_year: float,
    horizon_years: float = 100,
    *,
    step_years: float = 0.1,
    model: BernModel = DEFAULT_BERN_MODEL,
) -> float:
    _validate_non_negative_finite(start_year, "start_year")
    _validate_positive_finite(horizon_years, "horizon_years")
    _validate_positive_finite(step_years, "step_years")

    duration = horizon_years - start_year
    if duration <= 0:
        return 0.0

    integral = _integrate_trapezoid(model.impulse_response, 0.0, duration, step_years)
    return integral * model.radiative_efficiency


def crf_gas(
    start_year: float,
    horizon_years: float = 100,
    *,
    gas: GasName = "CO2",
    step_years: float = 0.1,
    model: BernModel | GasModel | None = None,
) -> float:
    selected_model = _resolve_gas_model(gas, model)
    _validate_non_negative_finite(start_year, "start_year")
    _validate_positive_finite(horizon_years, "horizon_years")
    _validate_positive_finite(step_years, "step_years")

    duration = horizon_years - start_year
    if duration <= 0:
        return 0.0

    integral = _integrate_trapezoid(selected_model.impulse_response, 0.0, duration, step_years)
    return integral * selected_model.radiative_efficiency


def dcf_co2(
    year: float,
    horizon_years: float = 100,
    *,
    step_years: float = 0.1,
    model: BernModel = DEFAULT_BERN_MODEL,
) -> float:
    _validate_non_negative_finite(year, "year")
    denominator = crf_co2(0.0, horizon_years, step_years=step_years, model=model)
    if denominator == 0:
        raise ValueError("horizon_years must produce a positive reference CRF")
    return crf_co2(year, horizon_years, step_years=step_years, model=model) / denominator


def dcf_gas(
    year: float,
    horizon_years: float = 100,
    *,
    gas: GasName = "CO2",
    step_years: float = 0.1,
    model: BernModel | GasModel | None = None,
) -> float:
    _validate_non_negative_finite(year, "year")
    denominator = crf_gas(0.0, horizon_years, gas=gas, step_years=step_years, model=model)
    if denominator == 0:
        raise ValueError("horizon_years must produce a positive reference CRF")
    return crf_gas(year, horizon_years, gas=gas, step_years=step_years, model=model) / denominator


def dcf_re2020(year: float) -> float:
    _validate_non_negative_finite(year, "year")
    if year > 50:
        return 0.580
    return 1.0 - 0.00842 * year


def static_gwp(flows: Iterable[Flow]) -> float:
    return sum(flow.amount * flow.gwp for flow in flows)


def dynamic_gwp(
    flows: Iterable[Flow],
    *,
    method: DynamicMethod = "bern",
    horizon_years: float = 100,
    step_years: float = 0.1,
    model: BernModel = DEFAULT_BERN_MODEL,
) -> float:
    if method not in {"bern", "re2020"}:
        raise ValueError("method must be either 'bern' or 're2020'")

    total = 0.0
    for flow in flows:
        if method == "bern":
            factor = dcf_co2(flow.year, horizon_years, step_years=step_years, model=model)
        else:
            factor = dcf_re2020(flow.year)
        total += flow.amount * flow.gwp * factor
    return total


def _integrate_trapezoid(function, start: float, end: float, step: float) -> float:
    if end == start:
        return 0.0

    total = 0.0
    current = start
    previous_value = function(current)

    while current < end:
        next_point = min(current + step, end)
        next_value = function(next_point)
        total += (previous_value + next_value) * (next_point - current) / 2
        current = next_point
        previous_value = next_value

    return total


def _resolve_gas_model(gas: GasName, model: BernModel | GasModel | None) -> BernModel | GasModel:
    if model is not None:
        return model
    if gas not in DEFAULT_GAS_MODELS:
        raise ValueError("gas must be one of 'CO2', 'CH4', or 'N2O'")
    return DEFAULT_GAS_MODELS[gas]


def _validate_finite(value: float, name: str) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _validate_non_negative_finite(value: float, name: str) -> None:
    _validate_finite(value, name)
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _validate_positive_finite(value: float, name: str) -> None:
    _validate_finite(value, name)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
