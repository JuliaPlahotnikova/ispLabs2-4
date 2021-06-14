import simplejson as json
import yaml
import toml
try:
    filename="convert"
    f = open(filename+'.toml', 'r')
    tomlData = toml.load(f)
    f.close()
except FileNotFoundError:('File not find')

ff = open("convert2"+'.json', 'w+')
jsonData = {'func':'\t', 'arr':'','null':'', 'bool1':'','bool2':'', 'string':'','fred':'', 'emptyArray':'','emptyObject':'', 'emptyString':''}
jsonData['func'] = tomlData['func']
jsonData['arr'] = tomlData['arr']
jsonData['null'] = tomlData['null']
jsonData['bool1'] = tomlData['bool1']
jsonData['bool2'] = tomlData['bool2']
jsonData['string'] = tomlData['string']
jsonData['fred'] = tomlData['fred']
jsonData['emptyArray'] = tomlData['emptyArray']
jsonData['emptyObject'] = tomlData['emptyObject']
jsonData['emptyString'] = tomlData['emptyString']
jsonData['code'] = tomlData['code']
jsonData['base64'] = tomlData['base64']
json.dump(jsonData, ff)