import importlib

FUNCTIONS = {}

def _import_function_if_necessary(function_id):
    def split_element_function(element):
        components = element.split(".")
        function_name = components[-1]
        module_name = "".join(components[:-1])
        return module_name, function_name

    if function_id in FUNCTIONS.keys():
        return

    mod_name, fun_name = split_element_function(function_id)
    mod = importlib.import_module(mod_name)
    fun = getattr(mod, fun_name)

    FUNCTIONS[function_id] = fun

def solve_element(task, requirement, element):
    """Apply an automatic step

    The element can be an automatic resolution or an automatic check.

    The element is an array.
        * The first item is the name of a function
        * The nexts items are arguments for this function

    The arguments of the function can be simple strings, being used as is, or
    another array, in which case it represent another function and recursion
    is used to get the result of this function before using it to execute the
    first function.

    If the step is an automatic check, this function should return a boolean
    representing if the requirement is fulfilled or not.

    If the element is an automatic resolution, it's returned value is
    irrelevant. If the automatic resolution failed it should throw an
    exception instead of returning a specific value.

    """

    _import_function_if_necessary(element[0])

    arguments = []
    for arg in element[1:]:
        if type(arg) == list:
            solved_arg = solve_element(task, requirement, arg)
            arguments.append(solved_arg)
        else:
            arguments.append(arg)

    return FUNCTIONS[element[0]](task, requirement, arguments)
