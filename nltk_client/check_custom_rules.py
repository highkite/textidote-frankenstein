import sys
sys.path.insert(0,'./pyStatParser')
from textidote import complete_check, get_next_sentence, set_advice
from stat_parser import Parser, display_tree

parser = Parser()

sentence = get_next_sentence()

def search_tree(tree, key_words):
    if isinstance(tree, str):
        if tree in key_words:
            return True
        else:
            return False

    for l in tree:
        if search_tree(l, key_words):
            return True

    return False

def smells_weird(sentence):
    tree = parser.parse(sentence)
    print(sentence)

    #display_tree(tree)
    if search_tree(tree, ["VBG", "WDT", "WP", "WP$", "WRB"]):
        display_tree(tree)
        print(">" * 20)
        print(sentence)

while sentence is not None:
    print(smells_weird(sentence))
        #set_advice(indices[0], f"transitions: {r['remark']}",r["start_pos"], r["end_pos"])

    sentence = get_next_sentence()

complete_check()
