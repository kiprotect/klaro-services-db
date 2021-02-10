import os
import json

labels = {}

def process_ref(data, parent):
    return lambda : labels[data['$ref']]

def process_label(data, parent):
    nd = data.copy()
    del nd['$label']
    labels[data['$label']] = nd
    return nd

def process_struct(data, parent=None):
    if isinstance(data, dict):
        func = None
        for k, v in data.items():
            if k.startswith('$') and f'process_{k[1:]}' in globals():
                func = k[1:]
                break
        if func:
            return globals()[f'process_{func}'](data, parent)
        d = {}
        for k, v in data.items():
            d[k] = process_struct(v, data)
        return d
    elif isinstance(data, (list, tuple)):
        return [process_struct(v, parent=data) for v in data]
    return data

def finalize_struct(data):
    if isinstance(data, dict):
        d = {}
        for k, v in data.items():
            if callable(v):
                print("calling...")
                d[k] = v()
            else:
                d[k] = finalize_struct(v)
        return d
    elif isinstance(data, (list, tuple)):
        return [finalize_struct(v) for v in data]
    elif callable(data):
        return data()
    return data

def process_db(filename):
    with open(filename) as input:
        database = json.load(input)
    return finalize_struct(process_struct(database))

db_filename = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.json"))

if __name__ == '__main__':
    result = process_db(db_filename)
    with open(db_filename, 'w') as output_file:
        json.dump(result, output_file, indent=2, sort_keys=True)