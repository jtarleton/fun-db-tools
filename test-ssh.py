#!/usr/bin/env python
from dotenv import load_dotenv
from pathlib import Path
import os
p=Path(os.getcwd())
os.chdir(p.parent)
p=Path(os.getcwd())
os.chdir(p.parent)
p2 = Path(os.getcwd())
p3= Path.joinpath(p2, '.env')
print(p3)
import os
load_dotenv(p3)

import paramiko
import logging
import subprocess
import platform



def check_env_vars():
  os.system("export PRIV_KEY_FILE");
  os.system("export PRIV_KEY_FILE_PASSPHRASE");
  os.system("export PROJECT_NAME");
  os.system("export ACQUIA_DEV_USER");
  os.system("export ACQUIA_DEV_HOST");
  
  priv_key_file = (os.getenv('PRIV_KEY_FILE'))
  passphrase = (os.getenv('PRIV_KEY_FILE_PASSPHRASE'))
  if not priv_key_file:
      print("Missing PRIV_KEY_FILE in .env file. Please copy .env.example to .env and fill in the information.")
      return True
  if not passphrase:    
      print("Missing PRIV_KEY_FILE_PASSPHRASE in .env file. Please copy .env.example to .env and fill in the information.")
      return True
  return False


def get_ssh_auth_error():
  priv_key_file = (os.getenv('PRIV_KEY_FILE'))
  passphrase = (os.getenv('PRIV_KEY_FILE_PASSPHRASE'))
  k = paramiko.RSAKey.from_private_key_file(priv_key_file, password=passphrase)
  paramiko.util.log_to_file('ssh.log') # sets up logging

  plat = platform.system()

  version = paramiko.__version__
  version_parts = version.split('.')
  if (int(version_parts[1]) < 12):
    print("Your paramiko version is " + '.'.join(version_parts))
    print("Please update to paramiko version 2.12.0 or newer.")
    if (plat == "Linux"):
      print("Linux:")
      print("sudo apt install python3-paramiko")
      cmd = "sudo apt install python3-paramiko"
    
    if (plat == "Darwin"):
      print("macOS:")
      print("sudo -H pip3 install paramiko --ignore-installed \nsudo -H pip install paramiko --ignore-installed")
      cmd = "sudo -H pip3 install paramiko --ignore-installed"
      
    val = input("Install now for platform " + plat + "? [Yes]")
    if (val != "No"  and val != "N" and val != "n" and val != "no") and (type("No") == type(val)):
      os.system(cmd)
      #subprocess.check_output([cmd])
    else:
      exit(1)

  ACQUIA_DEV_USER=".dev"
  ACQUIA_DEV_HOST="dev.ssh.prod.acquia-sites.com"

  hostname = (os.getenv('PROJECT_NAME') + ACQUIA_DEV_HOST)
  myuser = (os.getenv('PROJECT_NAME') + ACQUIA_DEV_USER)
  #logging.basicConfig(filename='ssh.log', filemode='w')
  #logging.getLogger("paramiko").setLevel(logging.ERROR)

  sshcon   = paramiko.SSHClient()  # will create the object
  sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #

  try:
    sshcon.connect(hostname, username=myuser, pkey=k) # no passwd needed
   
    sshtrans = sshcon.get_transport()
    is_auth = sshtrans.is_authenticated()


    sshtrans = sshcon.get_transport();
    is_auth = sshtrans.is_authenticated()

    print("Checking is_authenticated on transport.")
    if is_auth:
      commands = [ "hostname" ]
      for command in commands:
        stdin , stdout, stderr = sshcon.exec_command(command)

        stdout.channel.recv_exit_status()

        output = stdout.read()
        print(output.decode())
          
      sshtrans.close();
      # if authenticated, return False since there was no error.
      return False
    else:
      # Something wrong with auth state on the transport object, but no exception thrown.
      return 'Unknown error.'
  except Exception as e:
      return e

def main():
  bad_env_vars = check_env_vars()
  if bad_env_vars:
    # exit with non-zero on failure.
    exit(1)
  else:
    # exit with zero on success.
    print("You .env variables are configured correctly.")

  bad_auth = get_ssh_auth_error()
  if bad_auth:
    # exit with non-zero on failure.
    exit(bad_auth)
  else:
    # exit with zero on success.
    print("It appears Acquia is reachable and your SSH key is configured correctly.")
    exit(0)

# Run the SSH authentication and error check.
# Exit normally only if the authentication succeeded.
main()
