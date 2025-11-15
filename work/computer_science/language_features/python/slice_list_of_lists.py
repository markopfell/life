def slice_list_of_lists(list_of_lists):
    return list(zip(*list_of_lists))


a = [1, 2, 3]
b = [4, 5, 6]
print(slice_list_of_lists([a, b]))
# [(1, 4), (2, 5), (3, 6)]
