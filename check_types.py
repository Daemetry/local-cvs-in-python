from functools import wraps

def check_types(*expected_types):
    def decorator(f):
        @wraps(f)
        def wrapper(*args):
            if not _check(expected_types, args):
                raise TypeError
            return f(*args)
        return wrapper
    return decorator

def _check(expected, actual):
    if len(expected) != len(actual):
        return False

    for i in range(len(expected)):
        try:
            exp_iter = iter(expected[i])
            act_iter = iter(actual[i])
            if not isinstance(actual[i], type(expected[i])):
                return False
            if not _check(list(exp_iter), list(act_iter)):
                return False
        except TypeError:
            if not isinstance(expected[i], type):
                raise ValueError("Parameter given is not a type.")
            if not isinstance(actual[i], expected[i]):
                return False

    return True
        
