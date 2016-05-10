#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../

pip freeze
nosetests --with-cov --cover-package pyexcel --cover-package tests --with-doctest --doctest-extension=.rst tests README.rst pyexcel
if [ $? == 0 ] ; then
	rm tmp.db
else
    rm tmp.db
    exit 1;
fi
