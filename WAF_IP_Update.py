
#### Update WAF IP Setting ####

import boto3


def WAF_IP(IP):
    client = boto3.client('waf-regional')
    token = client.get_change_token()     #get token from local
    response = client.update_ip_set(
        IPSetId='a8288f39-5a7e-4b02-942d-7455a015a548',
        ChangeToken=token.get('ChangeToken'),     #use token
        Updates=[
            {
                'Action': 'INSERT',
                'IPSetDescriptor': {
                    'Type': 'IPV4',
                    'Value': IP,
                }
            },
        ]
    )
    return response


if __name__ == '__main__':   # test
    WAF_IP('1.1.1.1/32')
