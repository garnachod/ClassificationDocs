#!/bin/bash
sudo apt-get install python-virtualenv
sudo apt-get install libpq-dev
sudo apt-get install python-dev
sudo apt-get install libblas-dev liblapack-dev gfortran g++
sudo apt-get install build-essential
sudo apt-get install git
sudo apt-get install memcached
virtualenv venv
source venv/bin/activate
pip install -Ur requirements.txt
easy_install gensim[distributed]
pip install git+git://github.com/scikit-learn/scikit-learn.git
python setup.py install