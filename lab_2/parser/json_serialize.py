import inspect
import types

f_found = {}


def dumps_list(obj):
    if not len(obj):
        return "[]"
    res = "[\n"
    for i in range(len(obj) - 1):
        res += (_dumps(obj[i]) + ",\n")
    res += (_dumps(obj[-1]) + "\n]")
    return res


def dumps_dict(obj):
    if not len(obj):
        return "{}"
    res = "{\n"
    keys = list(obj)
    for i in keys[:-1]:
        res += (
                '"'
                + str(i)
                + '"'
                + ": "
                + _dumps(obj[i])
                + ",\n"
        )
    res += (
            '"'
            + str(keys[-1])
            + '"'
            + ": "
            + _dumps(obj[keys[-1]])
            + "\n}"
    )
    return res


def is_instance(obj):
    if not hasattr(obj, "__dict__"):
        return False
    if inspect.isroutine(obj):
        return False
    if inspect.isclass(obj):
        return False
    else:
        return True

def class_to_dict(cls):
    dpns = ()
    if len(cls.__bases__) != 0:
        for i in cls.__bases__:
            if i.__name__ != "object":
                dpns += (class_to_dict(i),)
    args = {}
    st_args = dict(cls.__dict__)
    if len(st_args) != 0:
        for i in st_args:
            if inspect.isclass(st_args[i]):
                args[i] = class_to_dict(st_args[i])
            elif inspect.isfunction(st_args[i]):
                if st_args[i] not in f_found:
                    args[i] = function_to_dict(st_args[i])
            elif is_instance(st_args[i]):
                args[i] = object_to_dict(st_args[i])
            elif isinstance(
                    st_args[i],
                    (
                            set,
                            dict,
                            list,
                            int,
                            float,
                            bool,
                            type(None),
                            tuple,
                    ),
            ):
                args[i] = st_args[i]
    return {"class_type": {"name": cls.__name__, "bases": dpns, "dict": args}}


def object_to_dict(obj):
    return {
        "instance_type": {
            "class": class_to_dict(obj.__class__),
            "vars": obj.__dict__,
        }
    }


def gather_gls(obj, obj_code):
    global f_found
    f_found[obj] = True
    gls = {}
    for i in obj_code.co_names:
        try:
            if inspect.isclass(obj.__globals__[i]):
                gls[i] = class_to_dict(obj.__globals__[i])
            elif inspect.isfunction(obj.__globals__[i]):
                if obj.__globals__[i] not in f_found:
                    gls[i] = function_to_dict(obj.__globals__[i])
            elif is_instance(obj.__globals__[i]):
                gls[i] = object_to_dict(obj.__globals__[i])
            elif isinstance(
                    obj.__globals__[i],
                    (set, dict, list, int, float, bool, type(None), tuple, str),
            ):
                gls[i] = obj.__globals__[i]
        except KeyError:
            pass
    for i in obj_code.co_consts:
        if isinstance(i, types.CodeType):
            gls.update(gather_gls(obj, i))
    return gls



def function_to_dict(obj):
    gls = gather_gls(obj, obj.__code__)

    return {
        "function_type": {
            "__globals__": gls,
            "__name__": obj.__name__,
            "__defaults__": obj.__defaults__,
            "__closure__": obj.__closure__,
        }
    }

def set_to_dict(obj):
    return {"set_type": list(obj)}


def frozenset_to_dict(obj):
    return {"frozenset_type": list(obj)}


def tuple_to_dict(obj):
    return {"tuple_type": list(obj)}

def _dumps(obj):
    global f_found
    if obj is None:
        return "null"
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    elif obj is float("Inf"):
        return "Infinity"
    elif obj is float("-Inf"):
        return "-Infinity"
    elif obj is float("NaN"):
        return "NaN"
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, bytes):
        return '"' + str(list(bytearray(obj))) + '"'
    elif isinstance(obj, str):
        return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
    elif isinstance(obj, set):
        return dumps_dict(set_to_dict(obj))
    elif isinstance(obj, frozenset):
        return dumps_dict(frozenset_to_dict(obj))
    elif isinstance(obj, tuple):
        return dumps_dict(tuple_to_dict(obj))
    elif isinstance(obj, list):
        return dumps_list(obj)
    elif isinstance(obj, dict):
        return dumps_dict(obj)
    elif inspect.isfunction(obj):
        res = dumps_dict(function_to_dict(obj))
        f_found = {}
        return res
    elif inspect.isclass(obj):
        return dumps_dict(class_to_dict(obj))
    elif is_instance(obj):
        return dumps_dict(object_to_dict(obj))
    else:
        raise TypeError()


def dumps(obj):
    res = _dumps(obj).replace("\n", "")
    res = res.replace('"[', '[')
    res = res.replace(']"', ']')
    return res


def dump(obj, fp):
    string = dumps(obj)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")


#deserialize

def parse_symbol(string, idx):
    if string[idx] == '"':
        obj, idx = parse_string(string, idx + 1)
    elif string[idx].isdigit() or (string[idx] == "-" and string[idx + 1].isdigit()):
        obj, idx = parse_digit(string, idx)
    elif string[idx] == "{":
        obj, idx = parse_dict(string, idx + 1)
    elif string[idx] == "[":
        obj, idx = parse_list(string, idx + 1)
    elif string[idx] == "n" and string[idx: idx + 4] == "null":
        obj = None
        idx += 4
    elif string[idx] == "t" and string[idx: idx + 4] == "true":
        obj = True
        idx += 4
    elif string[idx] == "f" and string[idx: idx + 5] == "false":
        obj = False
        idx += 5
    elif string[idx] == "N" and string[idx: idx + 3] == "NaN":
        obj = False
        idx += 3
    elif string[idx] == "I" and string[idx: idx + 8] == "Infinity":
        obj = float("Infinity")
        idx += 8
    elif string[idx] == "-" and string[idx: idx + 9] == "-Infinity":
        obj = float("-Infinity")
        idx += 9
    else:
        raise StopIteration(idx)
    return obj, idx



def parse_dict(string, idx):
    args = {}
    comma = False
    colon = False
    phase = False
    temp = None

    try:
        next_char = string[idx]
    except IndexError:
        raise StopIteration(idx)
    while True:
        if next_char == "}":
            break
        elif next_char == " " or next_char == "\n":
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            phase = False
            comma = False
        elif next_char == ":":
            if colon is False:
                raise StopIteration(idx)
            idx += 1
            phase = True
            colon = False
        elif not comma and not phase:
            if next_char == '"':
                obj, idx = parse_string(string, idx + 1)
                if obj in args:
                    raise StopIteration(idx)
                temp = obj
                phase = False
                colon = True
            else:
                raise StopIteration(idx)
        elif not colon and phase:
            obj, idx = parse_symbol(string, idx)
            args[temp] = obj

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError:
            raise StopIteration(idx)
    if not comma and not colon and len(args) != 0:
        raise StopIteration(idx)
    if "function_type" in args and len(args.keys()) == 1:
        return dict_to_func(args["function_type"]), idx + 1
    if "static_method_type" in args and len(args.keys()) == 1:
        return staticmethod(args["static_method_type"]), idx + 1
    if "class_method_type" in args and len(args.keys()) == 1:
        return classmethod(args["class_method_type"]), idx + 1
    if "class_type" in args and len(args.keys()) == 1:
        return dict_to_class(args["class_type"]), idx + 1
    if "instance_type" in args and len(args.keys()) == 1:
        return dict_to_obj(args["instance_type"]), idx + 1
    if "tuple_type" in args and len(args.keys()) == 1:
        return tuple(args["tuple_type"]), idx + 1
    if "frozenset_type" in args and len(args.keys()) == 1:
        return frozenset(args["frozenset_type"]), idx + 1
    if "set_type" in args and len(args.keys()) == 1:
        return set(args["set_type"]), idx + 1
    else:
        return args, idx + 1



def parse_string(string, idx):
    first = idx
    opened = False
    try:
        while string[idx] != '"' or opened:
            if string[idx] == "\\":
                opened = not opened
            else:
                opened = False
            idx += 1
    except IndexError:
        raise StopIteration(idx)
    return string[first:idx], idx + 1



def dict_to_class(cls):
    try:
        return type(cls["name"], cls["bases"], cls["dict"])
    except IndexError:
        raise StopIteration("Incorrect class")



def dict_to_obj(obj):
    try:

        def __init__(self):
            pass

        cls = obj["class"]
        temp = cls.__init__
        cls.__init__ = __init__
        res = obj["class"]()
        res.__dict__ = obj["vars"]
        res.__init__ = temp
        res.__class__.__init__ = temp
        return res
    except IndexError:
        raise StopIteration("Incorrect object")


def collect_funcs(obj, is_visited):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = attr
            is_visited = collect_funcs(attr, is_visited)
    return is_visited



def set_funcs(obj, is_visited, gls):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = True
            attr.__globals__.update(gls)
            is_visited = set_funcs(attr, is_visited, gls)
    return is_visited



def dict_to_func(obj):
    closure = None
    if obj["__closure__"] is not None:
        closure = obj["__closure__"]
    res = types.FunctionType(
        globals=obj["__globals__"],
        code=obj["__code__"],
        name=obj["__name__"],
        closure=closure,
    )
    try:
        setattr(res, "__defaults__", obj["__defaults__"])
    except TypeError:
        pass
    funcs = collect_funcs(res, {})
    funcs.update({res.__name__: res})
    set_funcs(res, {res.__name__: True}, funcs)
    res.__globals__.update(funcs)
    res.__globals__["__builtins__"] = __import__("builtins")
    return res



def parse_digit(string, idx):
    first = idx
    try:
        while (
                string[idx] == "."
                or string[idx].isdigit()
                or string[idx] == "e"
                or string[idx] == "E"
                or string[idx] == "-"
                or string[idx] == "+"
        ):
            idx += 1
    except IndexError:
        pass
    res = string[first:idx]
    try:
        return int(res), idx
    except ValueError:
        try:
            return float(res), idx
        except ValueError:
            raise StopIteration(idx)



def parse_list(string, idx):
    args = []
    comma = False

    try:
        next_char = string[idx]
    except IndexError:
        raise StopIteration(idx)
    while True:
        if next_char == "]":
            break
        elif next_char == " " or next_char == "\n":
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            comma = False
        elif not comma:
            obj, idx = parse_symbol(string, idx)
            args.append(obj)

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError:
            raise StopIteration(idx)
    if not comma and len(args) != 0:
        raise StopIteration(idx)
    return list(args), idx + 1



def loads(string):
    idx = 0
    try:
        while string[idx] == " " or string[idx] == "\n":
            idx += 1
    except IndexError:
        pass
    obj, idx = parse_symbol(string, idx)

    try:
        while True:
            if string[idx] != " " and string[idx] != "\n":
                raise StopIteration(idx)
            idx += 1
    except IndexError:
        pass
    return obj



def load(fp):
    try:
        with open(fp, "r") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")
    return loads(data)