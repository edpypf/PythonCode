import time

def time_it(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f'{func.__name__} took {int((end-start)*1000)}ms')
        return result
    return wrapper

# if you want to apply time_it whenever calling some_op, you can use @ decorator
@time_it
def some_op():
    print('Starting op')
    time.sleep(1)
    print('we are done')
    return 123

if __name__ == "__main__":
    # please be noticed that there's no () after some_op, as we passed in the funciton iself, not a result of function
    # the parentheses () after time_it(some_op) are used to call the function returned by time_it(some_op).
    time_it(some_op)()

    # if you want to apply time_it whenever calling some_op, you can use @ decorator
    # add @time_it before the "def some_op()"
    some_op()
