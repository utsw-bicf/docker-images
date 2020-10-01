FROM bicf/bicfbase:2.0.1
LABEL author="Jon Gesell"

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh && \
  bash Miniconda3-py37_4.8.3-Linux-x86_64.sh -p /miniconda -b && \
  rm Miniconda3-py37_4.8.3-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}

RUN conda config --add channels defaults && \
  conda config --add channels bioconda && \
  conda config --add channels conda-forge && \
  conda update -n base -c defaults -y conda

RUN pip3 install --upgrade pip

RUN pip3 install argparse==1.4.0
RUN conda install pandas=0.25.3