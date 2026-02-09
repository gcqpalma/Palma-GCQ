from decimal import Decimal, getcontext, ROUND_HALF_UP

# We set the engine to 120 digits so it can accurately judge even the 100-digit test.
getcontext().prec = 120

GOLD_STANDARD_PI = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128"

def get_pi(decimals, method='round'):
    full_pi = Decimal(GOLD_STANDARD_PI)
    
    if method == 'truncate':
        dot_index = GOLD_STANDARD_PI.find('.')
        cut_point = dot_index + 1 + decimals
        return Decimal(GOLD_STANDARD_PI[:cut_point])
    
    elif method == 'round':
        quantizer = Decimal(f"1e-{decimals}")
        return full_pi.quantize(quantizer, rounding=ROUND_HALF_UP)

def calculate_circumference(radius, pi_val):
    return Decimal(2) * pi_val * Decimal(radius)

# --- THE EXPERIMENT ---
ORBIT_RADIUS = 40_000_000_000
precisions_to_test = [20, 40, 60, 100]

# Calculate "Absolute Truth"
true_pi = Decimal(GOLD_STANDARD_PI)
true_circ = calculate_circumference(ORBIT_RADIUS, true_pi)

print(f"{'Decimals':<10} | {'Method':<10} | {'Difference':<30}")
print("=" * 70)

# --- THE LOOP ---
for p in precisions_to_test:
    
    # 1. Test Truncation
    pi_trunc = get_pi(p, method='truncate')
    circ_trunc = calculate_circumference(ORBIT_RADIUS, pi_trunc)
    error_trunc = abs(true_circ - circ_trunc)

    # 2. Test Rounding
    pi_round = get_pi(p, method='round')
    circ_round = calculate_circumference(ORBIT_RADIUS, pi_round)
    error_round = abs(true_circ - circ_round)

    # 3. Print Results for this level 
    print(f"{p:<10} | {'Trunc':<10} | {error_trunc:.110f}")
    print(f"{p:<10} | {'Round':<10} | {error_round:.110f}")
    
    print("-" * 70)

print("\nDONE! The error gets smaller as precision increases.")