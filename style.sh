#!/bin/bash
shopt -s globstar
for file in apocalypse_sim/**/*.py
do
    echo "________________________________"
    echo "$file"
    pycodestyle "$file"
    pydocstyle "$file"
    echo ""
done
