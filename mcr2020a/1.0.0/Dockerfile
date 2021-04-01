FROM bicf/bicfbase:2.0.2
LABEL author="Jon Gesell"

#Install MCR 2020a
RUN apt-get -qq update; \
    apt-get -qq install -y unzip xorg curl; \
    mkdir -p /mcr-install; \
    mkdir -p /opt/mcr; \
    wget https://ssd.mathworks.com/supportfiles/downloads/R2020a/Release/6/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020a_Update_6_glnxa64.zip -P /mcr-install; \
    unzip -q /mcr-install/MATLAB_Runtime_R2020a_Update_6_glnxa64.zip -d /mcr-install; \
    ./mcr-install/install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent; \
    rm -rf mcr-install

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH /opt/mcr/v98/runtime/glnxa64:/opt/mcr/v98/bin/glnxa64:/opt/mcr/v98/sys/os/glnxa64:/opt/mcr/v98/extern/bin/glnxa64
