# uri = base + /API_VERSION/HOSTEDZONE/ID
hosted_zone_id = 'Z08544881R40NMKVW923J'
'''
uri_base = 'route53.amazonaws.com/'
uri_API = '2013-04-01/'
hosted_zone_name = 'firebeez.online/'
'''
import boto3
import boto3.session
import botocore.config
import botocore.exceptions
import route53
import os

import requests
import sys
import yaml

# Yaml-Config File
yaml_file = open("config.yml", "r")
yaml_content = yaml.safe_load(yaml_file)

provider_list = []
config_list = {}

# Parse yaml-file
for config, value in yaml_content.items():
    if config == "providers":
        for provider in value:
            providerObj = {value[provider]['token'], provider}
            provider_list.append(providerObj)

    if config == "entries":
        for attr in value:
            for param, inp in attr.items():
                config_list.update({param: inp})

ChangeBatch = {
    'Changes': [
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
            #    'Name': yaml_content[0][1],
           #     'Type': yaml_content[1][4],
                'Region': 'us-east-1',
                'ResourceRecords': [
                    {
               #         'Value': yaml_content[1][3],
                    },
                ],
            }
        },
    ]
}

client = boto3.client(
    service_name='route53',
    aws_access_key_id='_',
    aws_secret_access_key='_'
    ) 

try:
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
except botocore.exceptions.NoAuthTokenError as error:
    raise error
except botocore.exceptions.ClientError as error:
    raise ValueError('The parameters you provided are incorrect: {}'.format(error))


for k,v in response.items():
    if k == 'ResourceRecordSets':
        j = 0
        for record in v:
            j += 1
            q =  (f"> Eintrag {j}: ")
            for k, item in record.items():
                if type(item) == list:
                    for records in item:
                        q = q + ((records['Value']))
                else:
                    q = q + (f'{k}: {item}, ')
            print(q)
    

'''

domain = 'domain.tld'
subdomain = 'subdomain_name'

def get_public_ip():
    r = requests.get('http://icanhazip.com')
    return r.text.rstrip()

fqdn = '%s.%s' % (subdomain, domain)
zone = route53.get_zone(domain)
arec = zone.get_a(fqdn)
new_value = get_public_ip()
datestr = '"Last update %s."' % datetime.utcnow().strftime('%Y-%m-%d %H:%M')

if arec:
        old_value = arec.resource_records[0]

        if old_value == new_value:
                print '%s is current. (%s)' % (fqdn, new_value)
                sys.exit(0)

        print 'Updating %s: %s -> %s' % (fqdn, old_value, new_value)

        try:
                zone.update_a(fqdn, new_value, 900)
                zone.update_txt(fqdn, datestr, 900)

        except DNSServerError:
                # This can happen if the record did not already exist. Let's
                # try to add_a in case that's the case here.
                zone.add_a(fqdn, new_value, 900)
                zone.add_txt(fqdn, datestr, 900)
else:
        zone.add_a(fqdn, new_value, 900)
        zone.add_txt(fqdn, datestr, 900)
        '''
        