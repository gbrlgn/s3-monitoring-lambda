#!/bin/bash


WORKDIR=$1
pip install slack_sdk -t $WORKDIR/lambda_function
