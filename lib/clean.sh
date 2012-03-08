#!/bin/sh

rm -rf ./build
rm -rf ./autobahnpush.egg-info
rm -rf ./dist
find . -name "*.pyc" -exec rm {} \;
