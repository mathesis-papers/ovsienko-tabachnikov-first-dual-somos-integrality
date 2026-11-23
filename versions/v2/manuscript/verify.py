import argparse
import csv
from fractions import Fraction
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def multiply(left, right):
    return left[0] * right[0], left[0] * right[1] + left[1] * right[0]


def power(value, exponent):
    if exponent == 0:
        return Fraction(1), Fraction(0)
    return value[0] ** exponent, exponent * value[0] ** (exponent - 1) * value[1]


def divide(numerator, denominator):
    assert denominator[0] != 0
    return (
        numerator[0] / denominator[0],
        (numerator[1] * denominator[0] - numerator[0] * denominator[1])
        / denominator[0] ** 2,
    )


def dual_orbit(power_product, power_middle, weight_product, weight_middle, initial, length):
    values = [(Fraction(1), Fraction(shadow)) for shadow in initial]
    for index in range(length - 4):
        product_term = power(multiply(values[index + 1], values[index + 3]), power_product)
        middle_term = power(values[index + 2], power_middle)
        numerator = add(
            multiply((1, weight_product), product_term),
            multiply((1, weight_middle), middle_term),
        )
        values.append(divide(numerator, values[index]))
    return values


def coefficient_orbit(power_product, power_middle, weight_product, weight_middle, initial, length):
    real = [Fraction(1)] * 4
    shadow = list(map(Fraction, initial))
    for index in range(length - 4):
        adjacent_product = real[index + 1] * real[index + 3]
        next_real = (adjacent_product ** power_product + real[index + 2] ** power_middle) / real[index]
        next_shadow = (
            power_product * adjacent_product ** (power_product - 1)
            * (real[index + 3] * shadow[index + 1] + real[index + 1] * shadow[index + 3])
            + weight_product * adjacent_product ** power_product
            + power_middle * real[index + 2] ** (power_middle - 1) * shadow[index + 2]
            + weight_middle * real[index + 2] ** power_middle
            - next_real * shadow[index]
        ) / real[index]
        real.append(next_real)
        shadow.append(next_shadow)
    return list(zip(real, shadow))


def integral(value):
    return value[0].denominator == 1 and value[1].denominator == 1


def run_checks():
    counts = dict(orbits=0, coefficient_matches=0, coprime_windows=0,
                  local_criteria=0, denominator_criteria=0, first_failure_criteria=0,
                  zero_obstruction_orbits=0, original_nonintegral_orbits=0)
    length = 10
    initials = list(product((-1, 0, 1), repeat=4))
    initials.extend([(4, -7, 11, -13), (-9, 0, 2, 17)])
    for power_product, power_middle in product(range(1, 4), range(1, 5)):
        for weight_product, weight_middle in product(range(-2, 3), repeat=2):
            obstruction = (2 * power_product - 2) * weight_middle - (power_middle - 2) * weight_product
            for initial in initials:
                values = dual_orbit(power_product, power_middle, weight_product, weight_middle, initial, length)
                comparison = coefficient_orbit(power_product, power_middle, weight_product, weight_middle, initial, length)
                assert values == comparison
                counts['orbits'] += 1
                counts['coefficient_matches'] += length
                assert all(value[0] > 0 and value[0].denominator == 1 for value in values)
                assert all(values[index + 1][0] > values[index][0] for index in range(3, length - 1))
                for index in range(length - 3):
                    assert all(gcd(int(values[left][0]), int(values[right][0])) == 1
                               for left, right in combinations(range(index, index + 4), 2))
                    counts['coprime_windows'] += 1
                for index in range(4, length - 4):
                    if all(integral(value) for value in values[index - 4:index + 4]):
                        assert integral(values[index + 4]) == (obstruction % int(values[index][0]) == 0)
                        divisor = int(values[index][0])
                        assert values[index + 4][1].denominator == divisor // gcd(divisor, obstruction)
                        counts['local_criteria'] += 1
                        counts['denominator_criteria'] += 1
                predicted = next((index + 4 for index in range(4, length - 4)
                                  if obstruction % int(values[index][0]) != 0), None)
                actual = next((index for index, value in enumerate(values) if not integral(value)), None)
                assert predicted == actual
                counts['first_failure_criteria'] += 1
                if obstruction == 0:
                    assert all(integral(value) for value in values)
                    counts['zero_obstruction_orbits'] += 1
                if weight_product == 0 and weight_middle == 1 and power_product >= 2:
                    assert all(integral(value) for value in values[:9])
                    assert not integral(values[9])
                    counts['original_nonintegral_orbits'] += 1
    first_family_example = dual_orbit(2, 1, 0, 1, (0, 0, 0, 0), length)
    second_family_example = dual_orbit(1, 1, 1, 0, (0, 0, 0, 0), length)
    assert first_family_example[9][1] == Fraction(212361888977416665298, 5)
    assert second_family_example[8][1] == Fraction(159, 2)
    zero_middle_rows = [
        (1, (-2, 1, 0, 1)), (3, (-2, -2, 2, 1)),
        (6, (-2, -2, -2, 4)), (24, (-12, 0, -4, 3)),
        (56, (-13, -16, 3, 2)), (Fraction(307, 3), (-14, -18, -18, 15)),
    ]
    for initial in initials:
        values = dual_orbit(1, 0, 1, 0, initial, length)
        assert values == coefficient_orbit(1, 0, 1, 0, initial, length)
        for index, (constant, coefficients) in enumerate(zero_middle_rows, start=4):
            assert values[index][1] == constant + sum(
                coefficient * shadow for coefficient, shadow in zip(coefficients, initial))
        assert all(integral(value) for value in values[:9])
        assert values[9][1].denominator == 3
    with Path(__file__).with_name('shadow-certificate.csv').open(newline='') as source:
        certificate = list(csv.DictReader(source))
    assert len(certificate) == 26
    values = dual_orbit(1, 2, 0, 0, (0, 0, 0, 1), 26)
    assert values == coefficient_orbit(1, 2, 0, 0, (0, 0, 0, 1), 26)
    pairs = []
    for index, row in enumerate(certificate):
        assert set(row) == {'n', 'a', 'b'} and int(row['n']) == index
        pair = int(row['a']), int(row['b'])
        assert pair == values[index]
        assert pair[0] > 0
        pairs.append(pair)
    assert pairs[:4] == [(1, 0), (1, 0), (1, 0), (1, 1)]
    for index in range(22):
        initial_real, initial_shadow = pairs[index]
        next_real, next_shadow = pairs[index + 4]
        left_real, left_shadow = pairs[index + 1]
        middle_real, middle_shadow = pairs[index + 2]
        right_real, right_shadow = pairs[index + 3]
        assert initial_real * next_real == left_real * right_real + middle_real ** 2
        assert initial_real * next_shadow + initial_shadow * next_real == (
            left_real * right_shadow + right_real * left_shadow
            + 2 * middle_real * middle_shadow)
    assert all(pairs[index][1] > 0 for index in range(3, 25))
    assert pairs[25][1] == -545740823162385126878041
    return {
        'status': 'pass',
        'arithmetic': 'exact rational arithmetic with Python fractions.Fraction',
        'scope': {
            'power_product': [1, 2, 3], 'power_middle': [1, 2, 3, 4],
            'weight_product': [-2, -1, 0, 1, 2], 'weight_middle': [-2, -1, 0, 1, 2],
            'initial_shadows': 'all 81 tuples in {-1,0,1}^4 and (4,-7,11,-13), (-9,0,2,17)',
            'indices': [0, 9],
        },
        'counts': counts,
        'additional_checks': {
            'zero_middle_exponent': {'p': 1, 'q': 0, 'u': 1, 'v': 0,
                                     'initial_tuples': len(initials), 'first_failure': 9,
                                     'denominator': 3, 'affine_rows_per_tuple': 6},
            'homogeneous_sign_certificate': {
                'p': 1, 'q': 2, 'u': 0, 'v': 0, 'initial': [0, 0, 0, 1],
                'indices': [0, 25], 'rows': len(pairs), 'exchange_pairs': 22,
                'first_negative_index': 25, 'hone_index': 24, 'b25': str(pairs[25][1])},
        },
        'examples': {
            'first_family_p2_q1_zero_initial_shadows_b9': str(first_family_example[9][1]),
            'second_family_p1_q1_zero_initial_shadows_b8': str(second_family_example[8][1]),
        },
        'coverage': 'Finite checks of the coefficient recurrence, real-part positivity and integrality, coprime windows, and the local divisibility equivalence. The infinite classification is established by the written proof in note.tex.',
    }


def main():
    parser = argparse.ArgumentParser(description='Exact finite checks for dual Somos integrality.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run_checks()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
