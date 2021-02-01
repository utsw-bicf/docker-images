FROM flywheel/matlab-mcr:v95

ADD utrack.zip /utrack.zip
RUN mkdir -p /execute && \
    unzip -d /execute utrack.zip && \
    rm /utrack.zip