FROM bicf/python3.7:2.0.2
LABEL author="Jon Gesell"

RUN wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.2.1-source.zip && \
  unzip hisat2-2.2.1-source.zip && \
  rm hisat2-2.2.1-source.zip && \
  pushdir hisat2-2.2.1 && \
  make && \
  popdir

ENV PATH=/hisat2-2.2.1/:${PATH}
