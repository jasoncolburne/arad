#!/usr/bin/bash

NODES=(identity reader reviewer administrator)

for NODE in "${NODES[@]}"
do
  TARGET=node-${NODE}
  rsync -v -r -d --delete --delete-excluded node-common/common ${TARGET}
  cp -v node-common/Dockerfile ${TARGET}
  cp -v node-common/.dockerignore ${TARGET}
done
