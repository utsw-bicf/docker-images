#!/bin/bash

#Used when adding a new Docker image to test

dockerFile=`find */*/*ocker*ile -maxdepth 0 -printf "%T@ %Tc %p\n" | sort -n | rev | cut -f1 -d ' ' | cut -f1,2,3 -d '/' | rev | tail -n1`
testFile="`echo ${dockerFile} | cut -f1,2 -d '/'`/unittest.yml";
dockerImage="bicf/`echo ${dockerFile} | cut -f1,2 -d '/' | tr -s '/' ':'`";
docker build -t ${dockerImage} -f ${dockerFile} --rm --no-cache .                                                                          docker image ls
python3 tests/imagecheck.py "--entrypoint '' bicf" ${testFile}
