install_python_modules:
	echo "Installing required python modules"
	pip2 install ptyprocess

all:
	install_python_modules