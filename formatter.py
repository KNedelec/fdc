import json

def format_list(list):
    '''
    return a stringified list
    '''
    string_list = ",".join(map(lambda x: f"{json.dumps(x)}", list))

    return f"[{string_list}]"
