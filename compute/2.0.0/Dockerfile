FROM bicf/nextflow20:2.0.1

#Setup prerequisites
RUN apt update && \
    apt install -y build-essential unzip pv perl make python3-matplotlib texlive-xetex && \
    apt clean

#Setup Perl
RUN cpan App::cpanminus && \
    cpanm List::MoreUtils Switch Getopt::Long

#Setup SRA Toolkit
RUN wget "http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.9.6-1/sratoolkit.2.9.6-1-centos_linux64.tar.gz" && \
    tar -xvzf sratoolkit.2.9.6-1-centos_linux64.tar.gz && \
    rm sratoolkit.2.9.6-1-centos_linux64.tar.gz
ENV PATH=/sratoolkit.2.9.6-1-centos_linux64/bin:${PATH}

#Setup FastQC
RUN conda install -c bioconda fastqc

#Setup MultiQC
RUN wget https://sourceforge.net/projects/libpng/files/zlib/1.2.9/zlib-1.2.9.tar.gz && \
    tar -xvf zlib-1.2.9.tar.gz && \
    rm zlib-1.2.9.tar.gz
WORKDIR /zlib-1.2.9
RUN ./configure && \
    make && \
    make install && \
    ln -s -f /usr/local/lib/libz.so.1.2.9/lib libz.so.1
WORKDIR /
RUN conda install -c bioconda pandoc && \
    pip3 install multiqc

#Setup for Azure
ADD azureblobworker.sh /opt/azureblobworker.sh
RUN pip3 install azure-cli && \
    chmod +x /opt/azureblobworker.sh