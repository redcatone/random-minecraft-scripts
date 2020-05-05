from itertools import combinations
from collections import defaultdict
import math

def sum_of_product_combinations(num_list):
    total_dict = {} # Key containing final sum of the two products; Value containing three nested lists: 1st) product pair, 2nd) product 1 factors, 3rd) product 2 factors
    for i in range(1, math.floor(len(num_list)/2) + 1): # Don't need to check past halfway as it will be the inverse of previous combinations
        combination_object = combinations(num_list, i) # Calculates all possible combinations of a certain size
        for factors_group1 in list(combination_object):
            product1 = 1 # Product is multiplied so start at 1 not 0
            product2 = 1
            factors_group2 = num_list.copy() # Factors of group 2 is original list minus factors of group 1
            for num1 in factors_group1: # Calculate product
                product1 *= num1
                factors_group2.remove(num1)
            for num2 in factors_group2:
                product2 *= num2
            
            total = product1 + product2
            products = [product1, product2]
            factors_group1 = list(factors_group1)
            if factors_group1 and factors_group2 not in total_dict.values(): # Don't allow duplicate entries
                total_dict[total] = [products, factors_group1, factors_group2] # [[product1, product2], [factors1], [factors2]]

    for key in sorted(total_dict, reverse = True): # Print dictionary in descending order by key
        print(f"Total is: {key:5} - Sizes are: {total_dict[key][0]} - Factors are: {total_dict[key][1]} and {total_dict[key][2]}")
    return total_dict

def output_txt(num_list):
    total_dict = sum_of_product_combinations(num_list)
    with open("output.txt", "w") as o:
        for key in sorted(total_dict, reverse = True): # Converts dictionary to list and writes to file in descending order by key
            o.write(f"Total is: {key:5} - Sizes are: {str(total_dict[key][0]):10} - Factors are: {total_dict[key][1]} and {total_dict[key][2]}\n")

if __name__ == "__main__":
    output_txt([2, 3, 5, 7, 11, 13])
