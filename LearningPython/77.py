def fibonacci(n):
    if n == 1:
        return 1
    if n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print("fibonacci(1):", fibonacci(1))
print("fibonacci(1):", fibonacci(2))
print("fibonacci(1):", fibonacci(3))
print("fibonacci(1):", fibonacci(4))
print("fibonacci(1):", fibonacci(5))