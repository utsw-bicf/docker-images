#!/bin/bash
module load singularity/3.0.2 parallel

mkdir -p /project/BICF/BICF_Core/shared/temp/singularity;
export SINGULARITY_CACHEDIR="/project/BICF/BICF_Core/shared/temp/singularity";
for i in `ls | grep "2\.0\.0"`; do
  image=`echo ${i} | sed -e "s:bicf\-:bicf/:g; s/\-2\.0\.0/:2\.0\.0/g; s/\.img//g"`;
  #echo "singularity build -F ${i} docker://${image}";
  singularity build -F ${i} docker://${image};
done #| shuf | parallel -j $[ `nproc` / 2 ];
#rm -rf /project/BICF/BICF_Core/shared/temp/singularity
