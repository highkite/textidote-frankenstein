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

from textidote import get_text
from py-grammark import check_wordiness

text = get_text()
res = check_wordiness(text)

print(res)
