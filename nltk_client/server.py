#from jsonrpcclient import parse, request
#import requests
#response = requests.post("http://localhost:8888/textidote", json=request("getLineCount"))
##response = requests.post("http://localhost:8888/textidote", json=request("getLines"))
#parsed = parse(response.json())
#print(parsed)
#
#line_count = parsed.result
#
#for i in range(line_count):
#    requ = request("getLine", params=(i,))
#    print(requ)
#    response = requests.post("http://localhost:8888/textidote", json=requ)
#    parsed = parse(response.json())
#    print(parsed.result)
#from textidote import get_next_sentence
#
#value = get_next_sentence()
#
#while value is not None:
#    print(value)
#    value = get_next_sentence()

from textidote import get_text, complete_check, translate_indices, set_advice
from grammark import check_wordiness

text_as_lines = get_text()
print(text_as_lines)
text = " ".join(text_as_lines)
print(text_as_lines)
res = check_wordiness(text_as_lines)

for r in res["findings"]:
    indices = translate_indices(r["start_pos"], r["end_pos"])
    print(indices)
    set_advice(indices[0], r["remark"], indices[1], indices[2])

complete_check()
