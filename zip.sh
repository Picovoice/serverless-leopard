#!/bin/bash

rm serverless_leopard.zip
pip install pvleopard --target ./serverless_leopard
cd serverless_leopard && zip -r ../serverless_leopard.zip ./ && cd ..
rm -rf ./serverless_leopard/pvleopard*