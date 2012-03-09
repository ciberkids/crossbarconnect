all: clean build upload

install:
	python setup.py install

clean:
	rm -rf ./autobahnpush.egg-info
	rm -rf ./build
	rm -rf ./dist

build:
	python setup.py bdist_egg

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_egg upload
	python setup.py bdist_wininst upload
