# -*- coding: utf-8 -*-

import socket, re, boto3

hostname = 'android.googleapis.com' #host name setting (one value only)
SG_ID = ['sg-0232439a1f53ac918', 'sg-0e60612ecc4c4cd55'] #Security Group ID's (list)
pattern = re.compile(r'\.'.join([r'\d{1,3}'] * 4))
result = pattern.findall(str(socket.gethostbyname_ex(hostname)))


# print (result)
# print(type(result))

def SG_egress(IP, host):
    client = boto3.client('ec2')
    for k in SG_ID:  #loop for multi value of security group id 
        response = client.authorize_security_group_egress(
            DryRun=False,
            GroupId=k,
            IpPermissions=[
                {'IpRanges': [{'CidrIp': IP, 'Description': host}],
                 'IpProtocol': 'tcp',
                 'FromPort': 443,
                 'ToPort': 443}]
        )


def SG_egress_revoke(IP):
    client = boto3.client('ec2')
    for j in SG_ID:
        response = client.revoke_security_group_egress(
            DryRun=False,
            GroupId=j,
            IpPermissions=[
                {'IpRanges': [{'CidrIp': IP}],
                 'IpProtocol': 'tcp',
                 'FromPort': 443,
                 'ToPort': 443}]
        )


client = boto3.client('ec2')
response = client.describe_security_groups(
    GroupIds=[SG_ID[0], ],
        DryRun=False,
)
describe_pattern = re.compile(r'\.'.join([r'\d{1,3}'] * 4) + r"/32', 'Description': '%s'" % hostname)
describe_pattern1 = re.compile(r'\.'.join([r'\d{1,3}'] * 4))
describe_result = describe_pattern.findall(str(response))
describe_result1 = describe_pattern1.findall(str(describe_result))  # Security Group added IP
addip = set(result).difference(set(describe_result1))
removeip = set(describe_result1).difference(set(result))


for i in addip:
    try:
        SG_egress("%s/32" % i, hostname)
    except:
        pass
for r in removeip:
    try:
        SG_egress_revoke("%s/32" % r)
    except:
        pass




