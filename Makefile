.PHONY: build clean upload all

build: src
	python3 -m build

clean:
	rm -rf dist

upload:
	twine upload dist/*.whl

all: build upload
