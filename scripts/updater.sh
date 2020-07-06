#!/bin/bash
OPTIND=1;
called=false;
oldImage="0.0.0";
currVer="0.0.0";
prevVer="0.0.0";
currImage="1.0.0";

#Print help message in case no file specified
print_usage() {
  echo -e "Usage: Used to do a cascade update of all images dependent on a specific docker file.  Example: bash dockerPath.sh -f [path to docker file for update] -m [Optional commit message (default 'Initial commit') -v [Version type: major, minor, patch]";
  exit 1;
}

#Set global variables
while getopts f:m:n:o:v:X flag; do
  case ${flag} in
    f) baseFile=${OPTARG};;
    m) commitMessage=${OPTARG};;
    v) versioning=${OPTARG};;
    X) called=true;;
    *) print_usage;;
  esac;
done;
shift $((OPTIND -1));

#Check for required variables
if [ -z ${baseFile} ]; then
  echo -e "Error: no path to updated Dockerfile found!  Please specify the Dockerfile path!\n"
  exit 1;
elif [ ! -r ${baseFile} ]; then
  echo -e "Error: file either does not exist, or is not readable!  Please verify that you have read permissions to ${baseFile}.\n"
  exit 2;
else
  baseFile=`readlink -e ${baseFile}`;
  basePath=`dirname ${baseFile}`;
  baseImage=`echo ${baseFile} | rev | cut -f2,3 -d '/' | tr -s '/' ':' | rev`;

  currImage=`echo ${baseImage} | cut -f1 -d ':'`;
  currVer=`echo ${baseImage} | cut -f2 -d ':'`;
  currMaj=`echo ${currVer} | cut -f1 -d '.'`;
  currMin=`echo ${currVer} | cut -f2 -d '.'`;
  currPat=`echo ${currVer} | cut -f3 -d '.'`;
  prevVer=`find ${basePath}/../* -maxdepth 0 -printf "%T@ %Tc %p\n" | sort -n | rev | cut -f1 -d ' ' | cut -f1 -d '/' | rev | tail -n2 | head -n1`;
  prevMaj=`echo ${currVer} | cut -f1 -d '.'`;
  prevMin=`echo ${currVer} | cut -f2 -d '.'`;
  prevPat=`echo ${currVer} | cut -f3 -d '.'`;
fi;

#Set default versioning and default commit message if also unset.
if [ -z "${versioning}" ]; then
  echo -en "Warning: Versioning type not set, ";
  if [ "${currVer}" == "${prevVer}" ]; then
    versioning="initial";
    echo "no previous versions detected, defaulting to 'initial'." ;
    if [ -z "${commitMessage}" ]; then
      commitMessage="Initial commit";
    fi;
  elif [ ${currMaj} -gt ${prevMaj} ]; then
    versioning="major";
    echo "major change detected, defaulting to 'major'.";
    if [ -z "${commitMessage}" ]; then
      commitMessage="Major update.  This version will be incompatible with previous images.";
    fi;
  elif [ ${currMin} -gt ${prevMin} ]; then
    versioning="minor";
    echo "minor change detected, defaulting to 'minor'.";
    if [ -z "${commitMessage}" ]; then
      commitMessage="Minor update.  This version will have minor changes in functionality, but should still be compatible with older versions.";
    fi;
  else
    versioning="patch";
    echo "patch detected, defaulting to 'patch'.";
    if [ -z "${commitMessage}" ]; then
      commitMessage="Patch.  Users should notice no significant changes when running versus previous versions.";
    fi;
  fi;
else
  versioning=${versioning,,};
  if [ -z "${commitMessage}" ]; then
    commitMessage="`echo ${versioning}` update.";
  fi;
fi;

#Setup the location variables
dockerDir=`echo ${baseFile} | rev | cut -f4- -d '/' | rev`;

#Kill and delete all partially built containers
for i in `docker image ls | tr -s ' ' ',' | grep "<none>" | cut -f3 -d ','`; do
  docker image rm -f ${i};
done;

#Run the Docker Build command on the file
docker build -t bicf/${baseImage} -f ${baseFile} --no-cache --rm .

#Find any images that use the old image version and increment them
for i in `find ${dockerDir}/*/*/* -type f`; do
  if [ `grep "^FROM bicf/${currImage}:${prevVer}" ${i} | wc -l` -gt 0 ]; then
    imagePath=`dirname ${i}`;
    newImage=`echo ${imagePath} | rev | cut -f2 -d '/' | rev`;
    oldVer=`echo ${imagePath} | rev | cut -f1 -d '/' | rev`;
    majVer=`echo ${oldVer} | cut -f1 -d '.'`;
    minVer=`echo ${oldVer} | cut -f2 -d '.'`;
    patVer=`echo ${oldVer} | cut -f3 -d '.'`;
    if [ "${versioning}" == "major" ]; then
      ((majVer++));
      minVer=0;
      patVer=0;
      newMessage="Major version change to ${baseImage}.";
    elif [ "${versioning}" == "minor" ]; then
      ((minVer++));
      patVer=0;
      newMessage="Minor version change to ${baseImage}.";
    else
      ((patVer++));
      newMessage="Patch performed on ${baseImage}.";
    fi;
    newVer=`echo "${majVer}.${minVer}.${patVer}"`;
    rsync -a ${imagePath}/* ${dockerDir}/${newImage}/${newVer}/;
    sed -ie "s/${currImage}:${prevVer}/${currImage}:${currVer}/g" ${dockerDir}/${newImage}/${newVer}/`basename ${i}`;
    bash updater.sh -f "${dockerDir}/${newImage}/${newVer}/`basename ${i}`" -v "$versioning" -m "${newMessage}";
  fi;
done;
