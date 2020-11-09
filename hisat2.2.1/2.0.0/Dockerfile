FROM bicf/python3.7:2.0.2
LABEL author="Jon Gesell"

RUN curl https://cloud.biohpc.swmed.edu/index.php/s/4pMgDq4oAF9QCfA/download > hisat2-2.2.1-Linux_x86_64.zip && \
  unzip hisat2-2.2.1-Linux_x86_64.zip && \
  rm hisat2-2.2.1-Linux_x86_64.zip && \
  pushdir hisat2-2.2.1 && \
  make && \
  popdir

ENV PATH=/hisat2-2.2.1/:${PATH}