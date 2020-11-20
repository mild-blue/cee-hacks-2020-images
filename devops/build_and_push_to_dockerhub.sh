#!/bin/bash
set -e

function build_and_push {
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
  echo "Building cee-hacks-2020-images-${1}."
  IMAGE_NAME="mildblue/cee-hacks-2020-images-${1}"
  docker build -t "${IMAGE_NAME}" -f "${DIR}/../Dockerfile.${1}" "${DIR}/.."
  echo "Pushing ${IMAGE_NAME}."
  docker push "${IMAGE_NAME}"
  echo "Done."
}

function build_and_push_worker {
  build_and_push "worker"
}

function build_and_push_backend {
  build_and_push "backend"
}