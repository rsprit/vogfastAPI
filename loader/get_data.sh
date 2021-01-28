#!/bin/bash

VERSION=${1:-latest}
TARGET=data

# create target directory

mkdir -p ${TARGET}

# clean up left-overs

cd ${TARGET}
rm -rf *

# fetch all files from source

wget -nv -r -np -nH -nd http://fileshare.csb.univie.ac.at/vog/${VERSION}/

# remove unneeded markup files

rm index.html*

# unzip FASTA files

gunzip *.fa.gz

# untar archives

for f in faa hmm raw_algs; do
	mkdir ${f}
	tar -x -z -C $f -f vog.$f.tar.gz
	rm vog.$f.tar.gz
done


