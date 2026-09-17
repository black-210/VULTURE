import pytest

from vulture.chemical_rf import ChemicalEquationSolver, MolecularRFAnalyzer


def test_water_equation_balances_exactly():
    result = ChemicalEquationSolver.balance_equation(
        [{"elements": {"H": 2}}, {"elements": {"O": 2}}],
        [{"elements": {"H": 2, "O": 1}}],
    )
    assert result["reactant_coefficients"] == [2, 1]
    assert result["product_coefficients"] == [2]


def test_nmr_proton_frequency_at_7_tesla():
    spectrum = MolecularRFAnalyzer().simulate_nmr_spectrum(7.0)
    assert spectrum["peaks"][0]["frequency_hz"] == pytest.approx(42.57747892e6 * 7.0)


def test_impedance_is_frequency_dependent_and_validated():
    analyzer = MolecularRFAnalyzer()
    analyzer.add_bond("H", "O", "single", 5.2, 0.957)
    low = analyzer.calculate_molecular_rf_impedance(1e6)
    high = analyzer.calculate_molecular_rf_impedance(10e6)
    assert low.real > 0
    assert abs(high.imag) < abs(low.imag)
    with pytest.raises(ValueError):
        analyzer.calculate_molecular_rf_impedance(0)


def test_bond_energy_frequency_is_not_reported_as_mhz():
    bond = MolecularRFAnalyzer().add_bond("C", "C", "double", 6.4, 1.34)
    assert bond.transition_frequency_hz > 1e14
