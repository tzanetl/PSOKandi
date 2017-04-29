
def asd():
    try:

        x = [1, 2, 0, 3]

        for i in range(len(x)):
            if x[i] == 0:
                raise ZeroDivisionError

        return x

    except ZeroDivisionError:
        x[i] = 55

        return x

def main():

    x = asd()

    print(x)
main()