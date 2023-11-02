


import re
 
def evaluate_expression(expression):
    # Extract numbers and operators from the expression string
    elements = re.findall(r'(\d+|\+|\-|\*|\/)', expression)
 
    # Initialize the result to the first number
    result = int(elements[0])
 
    # Apply each operator to the previous result and the current number
    for i in range(1, len(elements), 2):
        operator = elements[i]
        num = int(elements[i+1])
        if operator == '+':
            result += num
        elif operator == '-':
            result -= num
        elif operator == '*':
            result *= num
        elif operator == '/':
            result /= num
 
    return result

print(evaluate_expression("(6/3) * (6/2)"))
print(evaluate_expression("(10/12) * (150/1)"))
