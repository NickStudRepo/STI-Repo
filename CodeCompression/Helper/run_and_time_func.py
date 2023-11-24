import time

def run_and_time_function_1_1(func, func_parameter, name):
    start_time = time.time()
    res = func(func_parameter)
    finish_time = time.time()
    elapsed_time = (finish_time-start_time) * 1000 # this gets the time in ms
    elapsed_time_str = "{:.2f}".format(elapsed_time)
    print("Elapsed Time, " + name + ": " + elapsed_time_str + " ms")
    return res

def run_and_time_function_2_1(func, func_parameter1, func_parameter2, name):
    start_time = time.time()
    res = func(func_parameter1, func_parameter2)
    finish_time = time.time()
    elapsed_time = (finish_time-start_time) * 1000 # this gets the time in ms
    elapsed_time_str = "{:.2f}".format(elapsed_time)
    print("Elapsed Time, " + name + ": " + elapsed_time_str + " ms")
    return res

def run_and_time_function_1_2(func, func_parameter, name):
    start_time = time.time()
    res1, res2 = func(func_parameter)
    finish_time = time.time()
    elapsed_time = (finish_time-start_time) * 1000 # this gets the time in ms
    elapsed_time_str = "{:.2f}".format(elapsed_time)
    print("Elapsed Time, " + name + ": " + elapsed_time_str + " ms")
    return res1, res2

def print_time_infos(start_time, finish_time, name):
    elapsed_time = (finish_time-start_time) * 1000 # this gets the time in ms
    elapsed_time_str = "{:.2f}".format(elapsed_time)
    print("Elapsed Time, " + name + ": " + elapsed_time_str + " ms")