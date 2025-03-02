def timeit(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Czas wykonania funkcji {func.__name__}: {end-start}')
        return result
    return wrapper

def fib_rekurencja(n):
    if n < 2:
        return n
    return fib_rekurencja(n-1) + fib_rekurencja(n-2)
    
def fib_iteracyjnie(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    n = 6
    print(fib_iteracyjnie(n))
    print(fib_rekurencja(n))
    
    # pyinstrument --renderer=html --interval=0.0000000000000000000000001 fib.py