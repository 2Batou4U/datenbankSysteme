def collatz(n: int) -> bool:
    if n in (4, 2, 1):
        return True
    else:
        return collatz((n >> 1) if (n % 2 == 0) else (3 * n + 1))


n_in = 1
while True:
    print(f"{n_in}: {collatz(n_in)}")
    n_in += 1
