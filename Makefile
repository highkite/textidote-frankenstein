build:
	docker run --rm -i --user="$$(id -u):$$(id -g)" -v "$$PWD":/build textidote_build:latest

run:
	java -jar textidote.jar --check en --languagemodel en ./main.tex

clean:
	rm textidote.jar

run-docker:
	docker run --rm -i --user="$$(id -u):$$(id -g)" --net=none -v "$$PWD":/build -p 8888:8888 textidote_frankenstein:latest --check en --languagemodel en main.tex
