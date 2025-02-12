FROM ubuntu:22.04
LABEL maintainer="Jonathan LEGRAND <jonathan.legrand@ens-lyon.fr>"
LABEL corresponding_author="Peter Hanappe <peter@romi-project.eu>"
LABEL project="Robotics for microfarms"
LABEL homepage="https://docs.romi-project.eu/documentation/"
LABEL repository="https://github.com/romi/plant-3d-vision"
LABEL license="LGPL-3.0-or-later"
LABEL description="Python CGAL bindings for skeletonization."

# Set non-root user name:
ARG USER_NAME="romi"
ENV USER_ID=2020

# Variables required by Python:
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
# Variables required by `pip`:
ENV PATH="${PATH}:/home/${USER_NAME}/.local/bin"

# Change Shell to 'bash', default is 'sh':
SHELL ["/bin/bash", "-c"]
# Update package manager & install requirements:
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    build-essential \
    ca-certificates \
    gcc \
    libeigen3-dev \
    libcgal-dev \
    libgmp-dev \
    libmpfr-dev \
    mesa-utils \
    libosmesa6-dev \
    python3-dev \
    python3-pip \
    wget && \
    # Clean package manager:
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* && \
    # Create a non-root user named romi' and create a "home" folder wih proper rights:
    adduser --disabled-password --gecos '' --uid "${USER_ID}" "${USER_NAME}" && \
    chown -R ${USER_NAME}: /home/${USER_NAME}

# Change to non-root user:
USER ${USER_NAME}
# Change working directory:
WORKDIR /home/${USER_NAME}

# Copy the source files starting from the root folder (relative to context build):
COPY --chown=${USER_NAME} ./ ./romicgal/

RUN cd romicgal && \
    python3 -m pip install .[test] && \
    python3 -m pip cache purge

WORKDIR /home/${USER_NAME}/

CMD ["/bin/bash", "-c", "cd romicgal && pytest"]