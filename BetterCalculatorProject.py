num1 = int(input("Enter your first number: "))
op = input("Enter your operators(+,-,x,/): ")
num2 = int(input("Enter your second number: "))

if op == "+":
    print(num1 + num2)

elif op == "-":
    print(num1 - num2)


elif op == "x":
    print(num1 * num2)

elif op == "/":
    print(num1 / num2)

else:
    print("Invalid Operator")

