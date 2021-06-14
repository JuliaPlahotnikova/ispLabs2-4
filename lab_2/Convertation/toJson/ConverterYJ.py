import simplejson as json
import yaml
try:
    filename="convert"
    f = open(filename+'.yaml', 'r')
    yamlData = yaml.load(f)
    f.close()
except FileNotFoundError:('File not find')

ff = open("convert2"+'.json', 'w+')
jsonData = {'func':'\t', 'arr':'','null':'', 'bool1':'','bool2':'', 'string':'','fred':'', 'emptyArray':'','emptyObject':'', 'emptyString':''}
jsonData['func'] = yamlData['func']
jsonData['arr'] = yamlData['arr']
jsonData['null'] = yamlData['null']
jsonData['bool1'] = yamlData['bool1']
jsonData['bool2'] = yamlData['bool2']
jsonData['string'] = yamlData['string']
jsonData['fred'] = yamlData['fred']
jsonData['emptyArray'] = yamlData['emptyArray']
jsonData['emptyObject'] = yamlData['emptyObject']
jsonData['emptyString'] = yamlData['emptyString']
jsonData['code'] = yamlData['code']
jsonData['base64'] = yamlData['base64']
json.dump(jsonData, ff)