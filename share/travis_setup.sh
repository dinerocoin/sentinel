#!/bin/bash
set -evx

mkdir ~/.dinerocore

# safety check
if [ ! -f ~/.dinerocore/.dinero.conf ]; then
  cp share/dinero.conf.example ~/.dinerocore/dinero.conf
fi
