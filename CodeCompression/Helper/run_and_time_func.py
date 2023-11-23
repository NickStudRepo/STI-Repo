import time

def run_and_time_function(func, func_parameter, name):
    start_time = time.time()
    res = func(func_parameter)
    finish_time = time.time()
    elapsed_time = (finish_time-start_time) * 1000 # this gets the time in ms
    elapsed_time_str = "{:.2f}".format(elapsed_time)
    print("Elapsed Time, " + name + ": " + elapsed_time_str + " ms")
    return res