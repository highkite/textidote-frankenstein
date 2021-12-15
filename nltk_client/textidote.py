from jsonrpcclient import parse, request
import requests

host_name = "localhost"
port = 8888
sentence_cache = None
line_count = None
line_index = None

def configure_jsonrpc(_host_name="localhost", _port=8888):
    global port
    global host_name
    port = _port
    host_name = _host_name

def get_line_count():
    response = requests.post(f"http://{host_name}:{port}/textidote", json=request("getLineCount"))
    parsed = parse(response.json())
    return parsed.result

def get_line(i):
    requ = request("getLine", params=(i,))
    response = requests.post(f"http://{host_name}:{port}/textidote", json=requ)
    parsed = parse(response.json())
    return parsed.result

def get_text():
    """Returns the complete text
    """
    requ = request("getLines", params=(i,))
    response = requests.post(f"http://{host_name}:{port}/textidote", json=requ)
    parsed = parse(response.json())
    return parsed.result

def get_next_sentence():
    """ Returns the next sentence. If there is no such sentence it return None
    """
    global line_count
    global line_index
    global sentence_cache

    if line_count is None:
        line_count = get_line_count()

    if line_index is None:
        line_index = 0

# get line, that is not empty as first line
    if sentence_cache is None:
        sentence_cache = get_line(line_index)
        line_index += 1

        while sentence_cache == "":
            sentence_cache = get_line(line_index)
            line_index += 1

        if sentence_cache is None:
            return None

    # check if sentence cache contains whole sentence
    # TODO consider ?!;
    dot_index = sentence_cache.find(".")
    if dot_index != -1:
        sentence_to_return = sentence_cache[0:dot_index + 1].strip()
        sentence_cache = sentence_cache[dot_index + 1:].strip()
        return sentence_to_return
    else:
        next_line = get_line(line_index)
        line_index += 1

        if next_line == "":
            sentence_to_return = sentence_cache
            sentence_cache = None
            return sentence_to_return
        else:
            sentence_cache += " " + next_line.strip()
            return get_next_sentence()
