FROM bicf/python3.7:2.0.2
LABEL author="Jon Gesell"

RUN apt-get install -y autoconf automake curl perl zlib1g-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev libssl-dev libncurses5-dev bedtools

RUN conda install sambamba && \
    conda update sambamba

WORKDIR /usr/bin
RUN wget https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2 && \
    tar -vxjf htslib-1.9.tar.bz2 && \
    rm htslib-1.9.tar.bz2 
WORKDIR /usr/bin/htslib-1.9
RUN make && make install
WORKDIR /usr/bin

RUN wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2 && \
    tar -xvjf samtools-1.9.tar.bz2 && \
    rm samtools-1.9.tar.bz2
WORKDIR /usr/bin//samtools-1.9
RUN ./configure
RUN make && make install
WORKDIR /usr/bin

RUN wget https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2 && \
    tar -vxjf bcftools-1.9.tar.bz2 && \
    rm bcftools-1.9.tar.bz2
WORKDIR /usr/bin/bcftools-1.9
RUN make && make install
WORKDIR /

ENV PATH="/usr/bin/bcftools-1.9/bin:/usr/bin/htslib-1.9/bin:/usr/bin/samtools-1.9/bin:$PATH"