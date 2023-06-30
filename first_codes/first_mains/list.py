import statistics
store_clockwise_edoov_coefficient= []

def get_median():
    return statistics.median(store_clockwise_edoov_coefficient)

def add_clockwise_edoov_coefficient(item):
    store_clockwise_edoov_coefficient.append(item)

def get_list():
    return store_clockwise_edoov_coefficient