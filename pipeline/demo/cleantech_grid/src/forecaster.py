def forecast_grid_demand(base_mw: float, temp_c: float) -> float:
    if temp_c > 32.0:
        return round(base_mw * 1.35, 2)
    elif temp_c < 5.0:
        return round(base_mw * 1.25, 2)
    return round(base_mw, 2)
