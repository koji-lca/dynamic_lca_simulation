import math

import pytest

from dynamic_lca import Flow, crf_co2, dcf_co2, dcf_re2020, dynamic_gwp, impulse_response_co2, static_gwp


def test_impulse_response_at_zero_is_one():
    assert impulse_response_co2(0) == pytest.approx(1.0)


def test_impulse_response_rejects_negative_time():
    with pytest.raises(ValueError):
        impulse_response_co2(-1)


def test_dcf_at_zero_is_one():
    assert dcf_co2(0, horizon_years=100) == pytest.approx(1.0)


def test_dcf_decreases_for_later_emissions():
    dcf_0 = dcf_co2(0, horizon_years=100)
    dcf_50 = dcf_co2(50, horizon_years=100)
    dcf_100 = dcf_co2(100, horizon_years=100)

    assert dcf_0 > dcf_50 > dcf_100
    assert dcf_100 == pytest.approx(0.0)


def test_crf_reference_value_matches_report_scale():
    assert crf_co2(0, horizon_years=100) == pytest.approx(7.41e-14, rel=0.01)


def test_re2020_approximation_boundaries():
    assert dcf_re2020(0) == pytest.approx(1.0)
    assert dcf_re2020(50) == pytest.approx(1 - 0.00842 * 50)
    assert dcf_re2020(51) == pytest.approx(0.580)


def test_static_and_dynamic_gwp_for_delayed_emission():
    flows = [Flow(year=0, amount=-100), Flow(year=50, amount=100)]

    assert static_gwp(flows) == pytest.approx(0.0)
    assert dynamic_gwp(flows, method="re2020") == pytest.approx(-42.1)


def test_gwp_factor():
    flows = [Flow(year=10, amount=2, gwp=25)]

    expected = 2 * 25 * dcf_re2020(10)
    assert dynamic_gwp(flows, method="re2020") == pytest.approx(expected)


def test_dynamic_gwp_rejects_unknown_method():
    with pytest.raises(ValueError):
        dynamic_gwp([Flow(year=0, amount=1)], method="unknown")


def test_flow_rejects_negative_year():
    with pytest.raises(ValueError):
        Flow(year=-1, amount=1)


def test_flow_rejects_non_finite_amount():
    with pytest.raises(ValueError):
        Flow(year=0, amount=math.inf)
