# aws/gateway.py

def obtener_gateways(ec2):
    """Obtiene información de Internet Gateways (IGW) y NAT Gateways."""
    gateways_info = []

    # Internet Gateways
    igws = ec2.describe_internet_gateways()['InternetGateways']
    for igw in igws:
        vpc_ids = [attachment['VpcId'] for attachment in igw.get('Attachments', [])]
        gateways_info.append({
            'Gateway Type': 'Internet Gateway',
            'Gateway ID': igw['InternetGatewayId'],
            'VPCs Asociados': ', '.join(vpc_ids) if vpc_ids else 'Ninguno'
        })

    # NAT Gateways
    nat_gws = ec2.describe_nat_gateways()['NatGateways']
    for nat in nat_gws:
        gateways_info.append({
            'Gateway Type': 'NAT Gateway',
            'Gateway ID': nat['NatGatewayId'],
            'VPC ID': nat['VpcId'],
            'Subnet ID': nat['SubnetId'],
            'Estado': nat['State'],
            'IP Pública': nat.get('NatGatewayAddresses', [{}])[0].get('PublicIp', 'N/A')
        })

    return gateways_info
