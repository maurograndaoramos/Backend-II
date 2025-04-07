def linear_search(lst, target):
    for item in lst:
        if item == target:
            return True
    return False

my_list = [1, 2, 3, 4, 5]
print(linear_search(my_list, 3))
print(linear_search(my_list, 6))
