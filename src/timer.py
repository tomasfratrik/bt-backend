import time



def timeme(method):
    def wrapper(*args, **kw):
        startTime = time.time()
        result = method(*args, **kw)
        endTime = time.time()
        print(f"{method.__name__} took {endTime - startTime} seconds to execute")
        return result
    return wrapper