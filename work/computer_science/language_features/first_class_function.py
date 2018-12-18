def fun_1(first_class_fun):
    first_class_fun()
    first_class_fun()


def fun_2():
    print('At fun 2')

fun_1(fun_2)

# At fun 2
# At fun 2
