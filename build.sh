#!/bin/bash

set -x

docker build --build-arg FPM_VERSION=${FPM_VERSION}                  \
             --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
             --build-arg VCS_REF=$(git rev-parse --short HEAD)       \
             -t fg2it/fpm:${FPM_VERSION}${ITERATION}                 \
             .