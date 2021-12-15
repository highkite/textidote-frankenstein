TeXtidote-frankenstein: a turbulent hack that provides some benefits
==================================================================

Textidote is a grammar checker for latex files. You can find everything about
that here: https://github.com/sylvainhalle/textidote. It is a great tool and
I really wish I had learned about it earlier.

This here is not **textidote**, it is **textidote-frankenstein** and I mean
the monster.. and yes I know that the monster has no name and that it is 
actually the name of the doctor... but... um... yeah... alright, and with these 
conclusive arguments let's move on.

What is different in textidote-frankenstein?

- I extended textidote by a JSONrpc interface, that is called as a rule. The
idea is to let external tools interface with the grammar check. An additional 
benefit is that, we can incorporate external tools, that are based on
different programming languages than Java.
- I added a python library, that allows the easy interfacing with the JSONrpc
API and thus, allows to easily incorporate NLTK (natural language tool kit) in
a grammar check. Also, it represents kind of a reference implementation, if
you need the JSONRpc call details.
- I added rules that identify certain sentence constructions that my supervisor
did not like. This is probably only in my situation necessary, but maybe you
can adapt it to your purposes.
- I applied Grammark (https://github.com/highkite/py-grammark) and thus, had
a second 'grammar and readablity' check, that is more focused on scientific
writing, than the regular Language Tool library used by off-the-shelve
textidote.

This is only a quick hack, that I needed to improve the quality of some of my
writings. Maybe it is a starting point for someone, who wants to do something
similar. If you want to use it I advice you to use the docker files and please
note, that it is a bit shaky and was never intendet to operate smoothly.

# Run textidote-frankenstein

As mentioned I advise you to use the docker variant:

To build the docker container execute

```
docker build -t textidote_frankenstein:latest -f Dockerfile .
```

You can then run textidote either with make

```
make run-docker
```

or you can execute docker directly:

```
docker run --rm -i --user="$$(id -u):$$(id -g)" \
	--net=none -v "$$PWD":/build -p 8888:8888 \ 
	textidote_frankenstein:latest <latexfile in this dir>
```

Now JSONrpc is listening on port `localhost:8888`. At the moment there is no
arguments to change the port or host of the JSONrpc code. You need to do it in
program code if necessary: File: `JSONRpcServer.java` there is the call
`new InetSocketAddress(<change_port_here>)`.

## I'm a rebel and I don't want to use docker

Try your luck. I have it working with `openjdk 11.0.11`

```
java -jar textidote.jar <arguments>
```

# textidote.py - The python JSONrpc client

The python package is within the directory `nltk_client`. It is bascially
the file `textidote.py` and it uses the `requests` package and the
`jsonrpcclient` package.

The library offers the following methods to interact with textidote-frankenstein.


## configure_jsonrpc()

```
from textidote import configure_jsonrpc

# configure the host and port of the JSONRpc client
configure_jsonrpc(_host_name="localhost", _port=8888)
```

Although, you cannot configure the port or host in textidote-frankenstein with
commandline arguments yet, you can do it in the python client and only for the
client. It's almost useless. Isn't that great? Consistency is everything!

You propably do not need to call this method, since the default values are
those, that are implemented in textidote-frankenstein. And unless you change
these values in the textidote program code, they will be `localhost:8888`.

## get_line_count()

```
from textidote import get_line_count

# returns the number of cleaned lines that textidote extracted
line_count = get_line_count()
```

Textidote loads (nested) latex files cleanes it from its expressions and then
the text is splitted line-wise (based on '\n'). This is how the line count is
defined.

## get_line(\<line_index\>)

```
from textidote import get_line

# returns the first (1) line
line = get_line(1)
```

Returns the line with the given index. Lines are separated by `split("\n")`.
The total number of lines can be obtained with `get_line_count()`, such that
you can iterate through the lines. Note that one line is not necessarily one
sentence.

## get_next_sentence()

```
from textidote import get_next_sentence

# returns the next sentence (like an iterator) or None if there is no 'next'
# line. Tries to identify sentences.
line = get_next_sentence()
```

This method tries to return complete sentences. It determines the bounds of
those 'complete' sentences either by puncuation ".!?;" or if the next line
is an empty line. This is necessary, since for instance section titles are
rarely limited by punctuation.

## get_text()

```
from textidote import get_text

# returns the complete text
text = get_text()
```

There is not much more to say about this method. It is beautiful in its
simplicity. Take a moment and taste this flawless design.

## set_advice(\<line_index\>, \<remark\>, \<start_pos\>, \<end_pos\>)

```
from textidote import set_advice

# Add an advice to the second line referring the range from char 14 to 30
set_advice(2, 'This looks nasty', 14, 30)
```

Adds an advice.

## complete_check()

```
from textidote import complete_check

# Signal textidote, that you are finished
complete_check()
```

When this method is called, textidote will shutdown the JSONRpc server and
continue its regular grammar check.

# Two Example applications

In the following I introduce the two major applications for which I used this
hack. Those can be considered as examples and as starting points for your own
stuff.

## Grammark

The use case relies on the package `py-grammark`.

```
pip install py-grammark
```

## Check some custom rules

# Development

If you want to develop, there is a `Makefile`, that uses a docker instance
`textidot_build:latest` to build textidote with `ant`.

```
docker build -t textidote_build -f Dockerfile_build .
```

And then you can build the project with make

```
make build.
```

If you don't want to use docker you can alternatively install `openjdk 8`.

## How does it work
Sylvain Hallé did a beatiful job, when he engineered the application. Basically
textidote represents a toolchain. Every grammar checker is a tool, that is
registered in the toolchain. The toolchain is executed with the text, that we
want to test and then every tool applies its check, collects a number of 
`Advice` and then hands over the text to the next tool in the chain. After,
finishing the collected advice can be presented to the user.

Textidote differentiates two toolchains: The first operates on the original text,
i.e., the unaltered text, that still contains the latex or markdown expressions
and the second toolchain operates on the cleaned texts.

Rules, i.e., the tool registered in the toolchains, are children of the class
`Rule` and need to implement some methods. You can best learn that if you 
consider some of the existing rules.

To register a tool in the first toolchain you can call 
`linter.add(new <INamedMyRule>);` to add it to the second toolchain call
`linter.addCleaned(new <INamedMyRule>);`. You should probably to that in the
file `Main.java`. For now, the JSONRpcServer rule, that is the core of textidote
frankenstein is registered in the clean-toolchain.