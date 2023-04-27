all:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/* 

install:
	(cd ~ && sudo python3 -m pip install --upgrade mell)

uninstall:
	sudo pip uninstall mell -y

localinstall: uninstall all
	sudo pip install ./dist/mell-*-py3-none-any.whl

getdeps:
	python3 -m pip install --user --upgrade setuptools wheel
	python3 -m pip install --user --upgrade twine
	keyring --disable

test:
	(pytest --rootdir tests)

