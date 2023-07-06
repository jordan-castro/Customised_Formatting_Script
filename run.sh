#!/bin/bash

source envi/bin/activate

python custom_format.py "$@"

deactivate