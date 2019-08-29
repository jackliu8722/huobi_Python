#!/usr/bin/env bash

protoc -I=. --python_out=. market_downstream_protocol.proto
