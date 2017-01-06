#!/bin/bash

date_str=`date +%Y-%m-%d`

function usage
{
    echo "usage: mortgage [-h]"
}

while [ "$1" != "" ]; do
    case $1 in
        -h | --help )
            usage
            exit
            ;;
        * )
            usage
            exit 1
    esac
    shift
done

PYTHON=`which python3.4`
$PYTHON ~/Programming/Python/soup/mortgage.py

