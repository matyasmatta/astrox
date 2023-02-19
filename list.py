import statistics
store_edoov_coefficient= []

def get_median():
    return statistics.median(store_edoov_coefficient)

def add_edoov_coefficient(item):
    store_edoov_coefficient.append(item)

def get_list():
    return store_edoov_coefficient