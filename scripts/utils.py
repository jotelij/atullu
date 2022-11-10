import json
from pathlib import Path
from os import path as os_path
from brownie import config, network
import yaml

project_home = os_path.join(str(Path.home())   , "ba/atullu")     # python 3.5+

def network_support():
  support_json = config['tools']["chain"] + ".yaml"
  json_location = os_path.join(project_home, support_json)
  with open(json_location, "r") as f:
    support_config = yaml.load(f, Loader=yaml.CLoader)
  return support_config
  
def get_chain_data(network_chain=None):
  if network_chain is None:
    network_chain = config['networks'][network.show_active()]["chain"] if "chain" in config['networks'][network.show_active()] else "mainnet"
  json_location = os_path.join(project_home, 'data', network_chain + ".yaml")
  with open(json_location, "r") as f:
    support_config = yaml.load(f, Loader=yaml.CLoader)
  return support_config

def chain_data(network_chain=None):
  if network_chain is None:
    network_chain = config['networks'][network.show_active()]["chain"] if "chain" in config['networks'][network.show_active()] else "mainnet"
  json_location = os_path.join(project_home, 'data', network_chain + ".yaml")
  with open(json_location, "r") as f:
    support_config = yaml.load(f, Loader=yaml.CLoader)
  return (support_config["tokens"], support_config["routers"])

def get_tokens(network_chain=None):
  pass

def get_routers(network_chain=None):
  pass

def chain_blocked_tokens(network_chain=None):
  if network_chain is None:
    network_chain = config['networks'][network.show_active()]["chain"] if "chain" in config['networks'][network.show_active()] else "mainnet"
  json_location = os_path.join(project_home, 'config', "token_blacklist.json")
  with open(json_location, "r") as f:
    support_config = json.load(f)
  return support_config[network_chain]