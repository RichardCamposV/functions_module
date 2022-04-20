from time import sleep


def measure_length(iterable, *args, add_all=False):
    """
    def add(number1, number2):
        return number1 + number2

    print("Suma total = ", add(1, 3))
    """
    if args:
        length = [len(iterable)]
        for a in args:
            length.append(len(a))
        if add_all:
            length = sum(length)
        return length
    return len(iterable)


def suma(*args):
    return sum(args)


def main():
    print(measure_length("hola"))
    print(measure_length("hola", "como", "estas", add_all=True))
    print(suma(1, 2, 3, 4, 5))


if __name__ == "__main__":
    main()
