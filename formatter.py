import json

def format_list(list):
    '''
    return a stringified list
    '''
    print('list', list)
    print(json.dumps(list))
    string_list = ",".join(map(lambda x: f"{json.dumps(x, indent=2)}", list))

    return f"[{string_list}]"

def format(obj):
    return json.dumps(obj, indent=2)

def parse_list(string_list):
    return json.loads(string_list)
