from jsonrpcclient import parse, request
import requests
import re

host_name = "localhost"
port = 8888
sentence_cache = None
line_count = None
line_index = None

LINE_CACHE = None

def configure_jsonrpc(_host_name="localhost", _port=8888):
    """Configure _host_name and _port of the client.
    """
    global port
    global host_name
    port = _port
    host_name = _host_name

def get_line_count():
    """Returns the number of lines of the text
    """
    response = requests.post(f"http://{host_name}:{port}/textidote", json=request("getLineCount"))
    parsed = parse(response.json())
    return parsed.result

def get_line(i):
    """Returns the line with index 'i'
    """
    requ = request("getLine", params=(i,))
    response = requests.post(f"http://{host_name}:{port}/textidote", json=requ)
    parsed = parse(response.json())
    return parsed.result

def get_text(reset=False):
    """Returns the complete text
    With the reset flag it is possible to update the line cache
    """
    global LINE_CACHE
    if LINE_CACHE is not None and not reset:
        return " ".join(LINE_CACHE)

    requ = request("getLines")
    response = requests.post(f"http://{host_name}:{port}/textidote", json=requ)
    parsed = parse(response.json())
    LINE_CACHE = parsed.result
    return " ".join(LINE_CACHE)

def reset():
    """Resets the line cache
    """
    global LINE_CACHE
    LINE_CACHE = None

def translate_indices(start_pos, end_pos, lines = LINE_CACHE):
    """The get_text function returns a string. Identified positions within this text must
    be mapped back on line indicies and start/ end positions must lie within the sentence

    Returns line_index, new_start_pos, new_end_pos
    in this order
    """
    if lines is None:
        get_text()
        lines = LINE_CACHE

    line_index = 0
    new_start_pos = start_pos
    new_end_pos = end_pos
    start_set = False

    index_count = 0

    for line in lines:
        index_count += len(line)

        if not start_set and index_count >= new_start_pos:
            new_start_pos -= (index_count - len(line))
            start_set = True

        if index_count >= new_end_pos:
            new_end_pos -= (index_count - len(line))
            break

        line_index += 1
        index_count += 1 # add white space

    return line_index, new_start_pos, new_end_pos

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
    reg_result = re.search("[.;!?]", sentence_cache)
    dot_index = -1
    if reg_result is not None:
        dot_index = reg_result.start()
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

def set_advice(line_index, remark, start_pos, end_pos):
    """Sets a remark at line index with remark and start and end positions
    """
    requ = request("setAdvice", params=(line_index, remark, start_pos, end_pos))
    response = requests.post(f"http://{host_name}:{port}/textidote", json=requ)
    parsed = parse(response.json())
    return parsed.result

def complete_check():
    """Completes the check and let textidote continue
    """
    requests.post(f"http://{host_name}:{port}/textidote", json=request("completeCheck"))

