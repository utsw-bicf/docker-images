#!/bin/bash

OPTIND=1

#Print help message in case no file specified
print_usage() {
  echo -e "Usage: Used to do a cascade update of all images dependent on a specific docker file.  NOTE: DOES NOT INCRIMENT VERSIONS.  Example: bash dockerPath.sh -f [path to docker file for update] -m [Optional commit message (default 'Initial commit')";
  exit 1;
}

#Set global variables
while getopts f:m: flag; do
  case ${flag} in
    f) baseFile=${OPTARG};; 
    m) commitMessage=${OPTARG};;
    *) print_usage;;
  esac;
done;
shift $((OPTIND -1))

#Set default for unset variables
if [ -z ${commitMessage} ]; then
  commitMessage="Initial commit";
fi

#Set variables
baseFile=`readlink -e ${baseFile}`;
baseImage=`echo ${baseFile} | rev | cut -f2,3 -d '/' | tr -s '/' ':' | rev`;
dockerDir=`echo ${baseFile} | rev | cut -f4- -d '/' | rev`;

#Remove any partial images
for i in `docker image ls | tr -s ' ' ',' | grep "<none>" | cut -f3 -d ','`; do 
  docker image rm -f ${i}; 
done;

#Build the base image and commit
docker build -t bicf/${baseImage} -f ${baseFile} --no-cache --rm . &&
docker push bicf/${baseImage} &&
#git add ${baseFile} &&
#git commit -m ${commitMessage} &&
#git push origin master &&
for i in `find ${dockerDir}/*/*/* -type f`; do
  if [ `grep "^FROM bicf/${baseImage}" ${i} | wc -l` -gt 0 ]; then
    bash dockerPatch.sh -f `readlink -e ${i}` -m "Updated ${baseImage}"
  fi
done;
