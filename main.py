"""
PyDnsDNS
Author: Garbis Ciftci
Automatically update DNS records
"""

import json

import requests
import yaml

# Yaml-Config File
yaml_file = open("config.yml", "r")
yaml_content = yaml.safe_load(yaml_file)

# List's we'll be filling
provider_list = []
config_list = {}


# Main-Class 'Provider'
#   def __init__(self, <str>token, <str>provider)
#       initiate a 'Provider' object with necessary infos
class Provider:
    auth_token: str = ''
    url: str = ''

    def __init__(self, param_token: str, req_provider):
        print(f'> Initializing ({req_provider}) with token ({param_token})')
        self.auth_token = param_token
        match req_provider:
            case "digitalocean":
                self.url = 'https://api.digitalocean.com/'
            case "googledns":
                self.url = 'https://api.google.com/'
            case "route53":
                self.url = 'https://api.route53.com/'
            case _:
                print(f"No Configuration for {req_provider}")


# Main-Class 'Request'
# Child of 'Provider', adds functionality to the Provider (request handler)
#   def get_list(self)                          TODO: include all provider, split up functions per provider
#       retrieve all Domain records
#                                               TODO: update_list
#
class Request(Provider):
    def get_list(self):
        req_url = self.url
        req_dns = config_list["dns"]
        req_query = f'v2/domains/{req_dns}/records'
        print(f'   - Getting list of all records configured for domain: "{req_dns}" with: ')
        req_auth = self.auth_token
        req_header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + req_auth
        }
        print(f'     - Url: "{req_url}"')
        print(f'     - Query: "{req_query}"')
        print(f'     - Header: "{req_header}"')
        # if you dont wanna use up your credit, just replace r with prebuilt string and replace line #83-#82
        r = requests.get(req_url + req_query, headers=req_header)
        # r = '{"domain_records":[{"id":348461245,"type":"SOA","name":"@","data":"1800", "priority":null,"port":null,"ttl":1800,"weight":null,"flags":null,"tag":null},{"id":348461246,"type":"NS","name":"@","data":"ns1.digitalocean.com","priority":null,"port":null,"ttl":1800,"weight":null,"flags":null,"tag":null},{"id":348461247,"type":"NS","name":"@","data":"ns2.digitalocean.com","priority":null,"port":null,"ttl":1800,"weight":null,"flags":null,"tag":null},{"id":348461248,"type":"NS","name":"@","data":"ns3.digitalocean.com","priority":null,"port":null,"ttl":1800,"weight":null,"flags":null,"tag":null},{"id":348462595,"type":"A","name":"www","data":"127.0.0.1","priority":null,"port":null,"ttl":3600,"weight":null,"flags":null,"tag":null}],"links":{},"meta":{"total":5}}'
        return r

    def update_list(self, domain_record_id):
        req_url = self.url
        for k, v in config_list:
            if k == 'dns':
                req_query = f'/v2/domains/{v}/records/{domain_record_id}/records'
                req_dns = v
        print(f'   - Getting list of all records configured for domain: "{req_dns}" with: ')
        req_auth = self.auth_token
        req_header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + req_auth
        }
        print(f'     - Url: "{req_url}"')
        print(f'     - Query: "{req_query}"')
        print(f'     - Header: "{req_header}"')


# Parse yaml-file
for config, value in yaml_content.items():
    if config == "providers":
        for provider in value:
            providerObj = Provider(value[provider]['token'], provider)
            provider_list.append(providerObj)

    if config == "entries":
        for attr in value:
            for param, inp in attr.items():
                config_list.update({param: inp})

# cycle trough every provider configured, initiate base Provider parent-object and include Requesthandler-child
# fire Request.get_list with Provider Parent as param
for provider in provider_list:
    response = Request.get_list(provider)
    response_json = json.loads(response)
    # response_json = json.loads(response.text)
    j = 0
    print(f'     > Response:')
    for i in response_json['domain_records']:
        j += 1
        print(f'       - Entry Nr. {j}')
        print(
            f'          id: {i["id"]}, type: {i["type"]}, name: {i["name"]}, data: {i["data"]}, priority: {i["priority"]}, port: {i["port"]}, ttl: {i["ttl"]}, weight: {i["weight"]}, flags: {i["flags"]}, tag: {i["tag"]}')
        # if i["type"] == config_list["type"]:
        #     print(config_list["type"])
    j = 0
    print(f'     > Updating:')
    for i in response_json['domain_records']:
        j += 1
        print(f'        - # TODO Updating')
