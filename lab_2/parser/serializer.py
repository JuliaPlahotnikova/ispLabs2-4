import json_serialize
import toml_serialize
import yaml_serialize
import pickle_serialize

def _get_serializer(type):
    if type == "json":
        return json_serialize.dumps
    elif type == "toml":
        return toml_serialize.dumps
    elif type == "yaml":
        return yaml_serialize.dumps
    elif type == "pickle":
        return pickle_serialize.dumps
    else:
        raise ValueError(type)


def dumps(obj, type):
    _dumps = _get_serializer(type)
    return _dumps(obj)


def dump(obj, type, fp):
    string = dumps(obj, type)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")

    
def _get_deserializer(type):
    if type == "json":
        return json_serialize.loads
    elif type == "toml":
        return toml_serialize.loads
    elif type == "yaml":
        return yaml_serialize.loads
    elif type == "pickle":
        return pickle_serialize.loads
    else:
        raise ValueError(type)


def loads(str, type):
    _loads = _get_deserializer(type)
    return _loads(str)


def load(fp, type):
    try:
        with open(fp, "r") as file:
            str = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")
    return loads(str)