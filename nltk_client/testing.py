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

text = get_text()
print(text)
res = check_wordiness(text)

for r in res["findings"]:
    indices = translate_indices(r["start_pos"], r["end_pos"])
    print(indices)
    print(text[r["start_pos"] : r["end_pos"]])
    #set_advice(indices[0], r["remark"], indices[1], indices[2])
    set_advice(indices[0], f"wordiness: {r['remark']}",r["start_pos"], r["end_pos"])

complete_check()

##########################################
# Test translate_indices
##########################################

#test_list = ['', 'some text', ' and everything else', '', '', 'something']
#test_joined = " ".join(test_list)
#print(test_list)
#print(test_joined)
#print("Spaces replaced by %:")
#print(test_joined.replace(' ', '%'))
#
#start_pos = 16
#end_pos = 26
#
#print(f"start_pos: {start_pos}, end_pos: {end_pos}, substring: {test_joined[start_pos:end_pos]}")
#indices = translate_indices(start_pos, end_pos, test_list)
#print(f"Translated indices: {indices}")
#print(f"Extracted in list:{test_list[indices[0]][indices[1]:indices[2]]}")
