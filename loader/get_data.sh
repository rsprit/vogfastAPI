#!/bin/bash

SOURCE="http://fileshare.csb.univie.ac.at/vog"
TARGET=${1:-data}
VERSION=${2:-latest}

# create target directory

mkdir -p ${TARGET}

# clean up left-overs

cd ${TARGET}
rm -rf *

# fetch all files from source

wget -nv -r -np -nH -nd ${SOURCE}/${VERSION}/

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


