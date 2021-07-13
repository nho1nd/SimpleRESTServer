import json
import cherrypy

class DictionaryController(object):
    def __init__(self):
        self.myd = dict()

    def get_value(self, key):
        value = self.myd[key]
        return value


    # event handlers
    def GET_KEY(self, key):
        # rule 1: set up some default output
        output = {'result': 'success'}

        # rule 2: check your data and type - key and payload
        key = str(key)

        # rule 3: try - except blocks
        try:
            value = self.get_value(key)
            if value is not None:
                output['key'] = key
                output['value'] = value
            else:
                output['result'] = 'error'
                output['message'] = 'None type value associated with requested key'
        except KeyError as ex:
            output['result'] = 'error'
            output['message'] = 'key not found'
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)

    def PUT_KEY(self, key):
        output = {'result':'success'}
        key = str(key)
        #extract msg from body
        data = cherrypy.request.body.read()
        print(data)
        data = json.loads(data)

        try:
            val = data['value']
            self.myd[key] = val # do your local data update
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)

    def DELETE_KEY(self, key):
        output = {'result':'success'}
        key = str(key)
        
        try:
            del self.myd[key]
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        
        return json.dumps(output)

    def POST(self):
        output = {'result':'success'}
        #extract msg from body
        data = cherrypy.request.body.read()
        data = json.loads(data)

        try:
            key = data['key']
            val = data['value']
            self.myd[key] = val
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)

    def GET(self):
        try:
            temp = []
            for key, value in self.myd.items():
                temp.append({'key': key, 'value': value})
            
            output = {'entries': temp, 'result': 'success'}
        except KeyError as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)
