FROM bicf/java12:2.0.1
LABEL author="Jon Gesell"

#Install the dependencies for Singularity and Nextflow
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y libseccomp-dev pkg-config squashfs-tools cryptsetup libssl-dev uuid-dev python3.7 python3-pip curl

#Install Pip and Miniconda
ENV PATH="/miniconda/bin:${PATH}"
RUN wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda update -n base -c defaults -y conda && \
    pip3 install --upgrade pip && \
    pip3 install argparse==1.4.0 && \
    conda install pandas=0.25.3

#Install Singularity 3.6.0
ENV VERSION=1.13.5 OS=linux ARCH=amd64
ENV GOPATH=${HOME}/go PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin
RUN wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
    tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz && \
    curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh | sh -s -- -b ${GOPATH}/bin v1.15.0 && \
    mkdir -p ${GOPATH}/src/github.com/sylabs && \
    cd ${GOPATH}/src/github.com/sylabs && \
    git clone https://github.com/sylabs/singularity.git && \
    cd singularity && \
    git checkout v3.6.0-rc.3 && \
    cd ${GOPATH}/src/github.com/sylabs/singularity && \
    ./mconfig && \
    cd ./builddir && \
    make && \
    make install

#Install Nextflow 20.01.0
RUN mkdir -p nextflow20 && \
    cd nextflow20 && \
    wget -qO- https://get.nextflow.io | bash && \
    cd / && \
    chmod 755 -R /nextflow20

ENV PATH="/nextflow20:${PATH}"