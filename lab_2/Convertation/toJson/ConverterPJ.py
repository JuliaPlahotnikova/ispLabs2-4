import simplejson as json
import pickle
try:
    filename="convert"
    f = open(filename+'.pkl', 'rb')
    pickleData = pickle.load(f)
    f.close()
except FileNotFoundError:('File not find')


ff = open("convert2"+'.json', 'w+')
jsonData = {'func':'\t', 'arr':'','null':'', 'bool1':'','bool2':'', 'string':'','fred':'', 'emptyArray':'','emptyObject':'', 'emptyString':''}
jsonData['func'] = pickleData['func']
jsonData['arr'] = pickleData['arr']
jsonData['null'] = pickleData['null']
jsonData['bool1'] = pickleData['bool1']
jsonData['bool2'] = pickleData['bool2']
jsonData['string'] = pickleData['string']
jsonData['fred'] = pickleData['fred']
jsonData['emptyArray'] = pickleData['emptyArray']
jsonData['emptyObject'] = pickleData['emptyObject']
jsonData['emptyString'] = pickleData['emptyString']
jsonData['code'] = pickleData['code']
jsonData['base64'] = pickleData['base64']
json.dump(jsonData, ff)