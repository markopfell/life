def fun_1(first_class_fun, _kwargs):
    first_class_fun(_kwargs)
    first_class_fun(_kwargs)


def fun_2(_kwargs):
    print('At fun 2')
    print(_kwargs)


kwargs = {'first kwarg': 1, 'second kwarg': 2}
fun_1(fun_2, **kwargs)

# At fun 2
# {'first kwarg': 1, 'second kwarg': 2}
# At fun 2
# {'first kwarg': 1, 'second kwarg': 2}
