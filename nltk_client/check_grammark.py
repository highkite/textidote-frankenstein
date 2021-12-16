import argparse
from textidote import get_text, complete_check, translate_indices, set_advice
from grammark import check_wordiness, check_nominalizations, check_passive_voice, check_sentences, check_academic, check_transitions, check_grammar, check_eggcorns

parser = argparse.ArgumentParser(description='Execute the grammark checker with textidote over JSONRpc')
parser.add_argument('--all', dest='all', action='store_const', const=True, default=False, help='Execute all grammar checks')
parser.add_argument('--passive', dest='passive', action='store_const', const=True, default=False, help='Execute passive voice grammar checks')
parser.add_argument('--wordiness', dest='wordiness', action='store_const', const=True, default=False, help='Execute wordiness grammar checks')
parser.add_argument('--nominalizations', dest='nominalizations', action='store_const', const=True, default=False, help='Execute nominalizations grammar checks')
parser.add_argument('--sentences', dest='sentences', action='store_const', const=True, default=False, help='Execute sentences grammar checks')
parser.add_argument('--transitions', dest='transitions', action='store_const', const=True, default=False, help='Execute transitions grammar checks')
parser.add_argument('--academic', dest='academic', action='store_const', const=True, default=False, help='Execute academic grammar checks')
parser.add_argument('--grammar', dest='grammar', action='store_const', const=True, default=False, help='Execute grammar :) grammar checks')
parser.add_argument('--eggcorns', dest='eggcorns', action='store_const', const=True, default=False, help='Execute eggcorns grammar checks')
parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False, help='Prints the detected words in the text to compare them with the textidote output, to see if the offsets are correct.')

args = parser.parse_args()

text = get_text()

if args.all or args.passive:
    res = check_passive_voice(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"passive voice: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded passive voice check with score: {res['score']}")


if args.all or args.wordiness:
    res = check_wordiness(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"wordiness: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded wordiness check with score: {res['score']}")


if args.all or args.nominalizations:
    res = check_nominalizations(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"nominalizations: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded nominalizations check with score: {res['score']}")


if args.all or args.sentences:
    res = check_sentences(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"sentences: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded sentences check with score: {res['score']}")


if args.all or args.transitions:
    res = check_transitions(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"transitions: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded transitions check with score: {res['score']}")


if args.all or args.academic:
    res = check_academic(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"academic: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded academic check with score: {res['score']}")


if args.all or args.grammar:
    res = check_grammar(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"grammar: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded grammar check with score: {res['score']}")


if args.all or args.eggcorns:
    res = check_grammar(text)

    for r in res["findings"]:
        indices = translate_indices(r["start_pos"], r["end_pos"])
        if args.debug:
            print(r)
            print(text[r["start_pos"] : r["end_pos"]])

        set_advice(indices[0], f"eggcorns: {r['remark']}",r["start_pos"], r["end_pos"])

    print(f"Concluded eggcorns check with score: {res['score']}")

complete_check()
