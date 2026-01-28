from mobile_calc import calc_povo_monthly_cost, calc_linemo_monthly_cost, choose_best_plan

def test_case_8gb_30calls():
    result = choose_best_plan(8, 30)
    assert result["recommended"] == "povo"
    assert result["povo_cost"] == 2713
    assert result["linemo_cost"] == 2970

def test_case_1gb_nocall():
    result = choose_best_plan(1, 0)
    assert result["recommended"] == "povo"
    assert result["povo_cost"] == 390
    assert result["linemo_cost"] == 990

def test_case_30gb_nocall():
    result = choose_best_plan(30, 0)
    assert result["recommended"] == "povo"
    assert result["povo_cost"] == 2480
    assert result["linemo_cost"] == 2970