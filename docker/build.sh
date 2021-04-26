#!/bin/bash

###############################################################################
# Example usages:
###############################################################################
# 1. Default build options will create `roboticsmicrofarms/romicgal:latest` pointing at ROMI database:
# $ ./build.sh
#
# 2. Build image with 'debug' image tag & another 'romicgal' branch options:
# $ ./build.sh -t debug -b 'feature/faster_docker'

user=$USER
vtag="latest"
branch='master'
api_url='https://db.romi-project.eu'
docker_opts=""

usage() {
  echo "USAGE:"
  echo "  ./build.sh [OPTIONS]
    "
  echo "DESCRIPTION:"
  echo "  Build a docker image named 'roboticsmicrofarms/romicgal' using Dockerfile in same location.
    "
  echo "OPTIONS:"
  echo "  -t, --tag
    Docker image tag to use, default to '$vtag'."
  echo "  -u, --user
    User name to create inside docker image, default to '$user'."
  echo "  -b, --branch
    Git branch to use for cloning 'romicgal' inside docker image, default to '$branch'."
  # Docker options:
  echo "  --no-cache
    Do not use cache when building the image, (re)start from scratch."
  echo "  --pull
    Always attempt to pull a newer version of the parent image."
  # General options:
  echo "  -h, --help
    Output a usage message and exit."
}

while [ "$1" != "" ]; do
  case $1 in
  -t | --tag)
    shift
    vtag=$1
    ;;
  -u | --user)
    shift
    user=$1
    ;;
  -b | --branch)
    shift
    branch=$1
    ;;
  --no-cache)
    shift
    docker_opts="$docker_opts --no-cache"
    ;;
  --pull)
    shift
    docker_opts="$docker_opts --pull"
    ;;
  -h | --help)
    usage
    exit
    ;;
  *)
    usage
    exit 1
    ;;
  esac
  shift
done

# Get the date to estimate docker image build time:
start_time=`date +%s`

# Start the docker image build:
docker build -t roboticsmicrofarms/romicgal:$vtag $docker_opts \
  --build-arg USER_NAME=$user \
  --build-arg BRANCH=$branch \
  .

# Print docker image build time:
echo
echo "Build time: $(expr `date +%s` - $start_time)s"
