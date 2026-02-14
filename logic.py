import math

def calculate_power(current, voltage, power_factor, phases):
    if not (0 <= power_factor <= 1):
        raise ValueError("Power factor must be\nbetween 0 and 1")

    sin_phi = math.sqrt(1 - power_factor**2)

    if phases == 1:
        nominal_voltage = 230
        min_v, max_v = 1, 359                             #TBD for DC calculations 

    elif phases == 2:
        nominal_voltage = 400
        min_v, max_v = 360, 440

    elif phases == 3:
        nominal_voltage = 400
        min_v, max_v = 360, 440

    else:                                               
        raise ValueError("Invalid number of phases")

    # check range
    if not (min_v <= voltage <= max_v):
        voltage = nominal_voltage

    # calulate from INPUT/changed voltage
    if phases == 3:
        apparent_power = math.sqrt(3) * voltage * current
    else:
        apparent_power = voltage * current

    active_power = apparent_power * power_factor
    reactive_power = apparent_power * sin_phi

    return {
        "P": round(active_power, 2),
        "S": round(apparent_power, 2),
        "Q": round(reactive_power, 2),
        "voltage": voltage,
    }