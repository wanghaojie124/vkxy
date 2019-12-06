import time

test = [i for i in range(-1, 10)]
while len(test) > 0:
    for i in test:
        try:
            print(2/i)
            test.remove(i)
            print(test)
        except Exception as e:
            print(e)
            test.remove(i)