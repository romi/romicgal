FROM continuumio/miniconda3:latest
LABEL maintainer="Jonathan LEGRAND <jonathan.legrand@ens-lyon.fr>"

ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Set non-root user name:
ARG USER_NAME=scanner
ARG BRANCH=master

USER root
# Change shell to 'bash', default is 'sh'
SHELL ["/bin/bash", "-c"]
# Update package manager & install requirements:
RUN apt-get update && \
    apt-get install -yq --no-install-recommends git ca-certificates wget \
    build-essential libeigen3-dev libboost-dev libgmp-dev libmpfr-dev && \
    apt-get clean -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m ${USER_NAME} && \
    cd /home/${USER_NAME} && \
    chown -R ${USER_NAME}: /home/${USER_NAME}

# Change user
USER ${USER_NAME}
# Change working directory:
WORKDIR /home/${USER_NAME}

RUN git clone --branch $BRANCH https://github.com/romi/romicgal.git && \
    cd romicgal && \
    python -m pip install -e .

WORKDIR /home/${USER_NAME}/

CMD ["/bin/bash", "-c", "python romicgal/test.py"]