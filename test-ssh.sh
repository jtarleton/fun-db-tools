#!/bin/bash
python3 $PWD/test-ssh.py
# $? =  is the exit status of the most recently-executed command;
# by convention, 0 means success and anything else indicates failure.
if [ $? -eq 0 ]
then
  echo ""
else
  # Redirect stdout from echo command to stderr.
  echo "Script exited with error."
 # >&2
fi
