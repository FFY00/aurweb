#!/bin/sh
pytest --tap-stream "$(dirname "$0")/../aurweb/test/test_rpc.py"
