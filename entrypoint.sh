#!/bin/bash

cmd="$@"

sleep 5
alembic upgrade head
exec $cmd
