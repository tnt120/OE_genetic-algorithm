def binary_to_float(binary_str, value_range, bit_length):
    min_val, max_val = value_range
    int_val = int(binary_str, 2)
    max_int = 2**bit_length - 1
    return min_val + (int_val / max_int) * (max_val - min_val)

def float_to_binary(value, value_range, bit_length):
    min_val, max_val = value_range
    scaled = int((value - min_val) / (max_val - min_val) * (2**bit_length - 1))
    return format(scaled, f'0{bit_length}b')

def fitness_function(decoded):
    return -sum(x**2 for x in decoded)