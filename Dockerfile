FROM python:3
# developer Dockerfile for mesa development, installs from local git checkout
LABEL maintainer="Allen Lee <allen.lee@asu.edu>"

ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /opt/sim

COPY /apocalypse_sim /opt/sim

COPY requirements.txt ./

RUN apt-get update &&\
    apt-get install -y \
        make \
        gcc \
        libgdal20 libgdal-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8521

CMD ["mesa", "runserver"]

