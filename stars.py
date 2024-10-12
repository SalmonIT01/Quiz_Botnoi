def create_star(x):
    result = ""
    
    for i in range(1, x + 1):
        result += "*" * i + "\n"
    
    for i in range(x - 1, 0, -1):
        result += "*" * i + "\n"
    return result


x = input("Enter number: ")
print(create_star(int(x)))