FROM bicf/bicfbase:2.0.2

RUN apt-get update; \
    apt-get install -y unzip xorg curl x11-apps libxt6; \
    mkdir -p /execute; \
    (mkdir -p /opt/mcr && \
    mkdir -p /mcr-install && \
    wget https://ssd.mathworks.com/supportfiles/downloads/R2020a/Release/6/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020a_Update_6_glnxa64.zip -P /mcr-install; \
    unzip -q /mcr-install/MATLAB_Runtime_R2020a_Update_6_glnxa64.zip -d /mcr-install; \
    ./mcr-install/install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent; \
    rm -rf mcr-install;) & \
    (wget --no-check-certificate https://cloud.biohpc.swmed.edu/index.php/s/3DswCQyjf35G3YC/download -O download.zip; \
    unzip download.zip; \
    mv for_testing /execute/utrack; \
    chmod +x /execute/utrack/run_utrack.sh /execute/utrack/utrack; \
    rm download.zip;) & \
    wait;

ENV LD_LIBRARY_PATH /opt/mcr/v98/runtime/glnxa64:/opt/mcr/v98/bin/glnxa64:/opt/mcr/v98/sys/os/glnxa64:/opt/mcr/v98/extern/bin/glnxa64