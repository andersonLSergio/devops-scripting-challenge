#!/bin/bash
# ensure that the local venv includes all dependencies
# pip freeze > requirements.txt

# build aux docker image
docker build -t buildit4me:test .

# run aux container in interactive mode
docker run -it --rm --name buildit4me buildit4me:test /bin/bash