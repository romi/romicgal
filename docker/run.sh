#!/bin/bash

# Docker image tag to use, 'latest' by default:
vtag="latest"

usage() {
  echo "USAGE:"
  echo "  ./run.sh [OPTIONS]
    "
  echo "DESCRIPTION:"
  echo "  Start the romicgal container.
  Uses the docker image: 'roboticsmicrofarms/romicgal'.
    "
  echo "OPTIONS:"
  echo "  -t, --tag
    Docker image tag to use, default to '$vtag'."
  echo "  -h, --help
    Output a usage message and exit."
}

while [ "$1" != "" ]; do
  case $1 in
  -t | --tag)
    shift
    vtag=$1
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

docker run -it roboticsmicrofarms/romicgal:$vtag
