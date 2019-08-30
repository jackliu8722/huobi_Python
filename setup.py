#!/usr/bin/env python3
from setuptools import setup

setup(
    name="huobi-client",
    version="0.2",
    packages=['huobi', 'huobi.base','huobi.impl', 'huobi.impl.utils', 'huobi.exception', 'huobi.model', 'huobi.model_proto', 'huobi.protodecode'],
    install_requires=['requests', 'apscheduler', 'websocket-client', 'urllib3', 'protobuf']
)

