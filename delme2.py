from toolz import map

test_str_list = ["a", "b", "c"]
test_str_list2 = ["x", "y", "z"]


def upper(x):
    return x.upper()


print(list(map(str.upper, test_str_list)))
