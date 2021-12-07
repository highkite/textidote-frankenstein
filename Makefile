build:
	docker run --rm -i --user="$$(id -u):$$(id -g)" -v "$$PWD":/build textidote_build:latest

run:
	java -jar textidote.jar ./main.tex

clean:
	rm textidote.jar
