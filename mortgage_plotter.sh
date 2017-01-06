#!/bin/bash

freq_str="weekly"

function usage
{
    echo "usage: mortgage_plotter [[[-f weekly] | [--frequency weekly]] | [-h]]"
}

while [ "$1" != "" ]; do
    case $1 in
        -f | --frequency )
            shift
            if [ ! -z "$1" ]; then
                if [ "$1" == "weekly" ]; then
                    freq_str=$1
                elif [ "$1" == "monthly" ]; then
                    freq_str=$1
                else
                    freq_str="weekly"
                fi
            fi
            ;;
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
$PYTHON /Users/yamin/Programming/Python/soup/mortgage_plotter.py "$freq_str"

