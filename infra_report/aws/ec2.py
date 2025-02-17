def obtener_ec2(ec2):
    """Obtiene información de instancias EC2."""
    ec2_info = []
    instances = ec2.describe_instances()['Reservations']
    for reservation in instances:
        for instance in reservation['Instances']:
            grupos_seguridad = [sg['GroupName'] for sg in instance['SecurityGroups']]
            ec2_info.append({
                'Instance ID': instance['InstanceId'],
                'State': instance['State']['Name'],
                'Type': instance['InstanceType'],
                'Public IP': instance.get('PublicIpAddress', 'N/A'),
                'Private IP': instance.get('PrivateIpAddress', 'N/A'),
                'AZ': instance['Placement']['AvailabilityZone'],
                'Security Groups': ', '.join(grupos_seguridad)
            })
    return ec2_info

def obtener_vpcs(ec2):
    """Obtiene información de las VPCs."""
    vpcs_info = []
    vpcs = ec2.describe_vpcs()['Vpcs']
    for vpc in vpcs:
        vpcs_info.append({
            'VPC ID': vpc['VpcId'],
            'CIDR': vpc['CidrBlock'],
            'Estado': vpc['State']
        })
    return vpcs_info

def obtener_subredes(ec2):
    """Obtiene subredes con Tags y clasificación pública/privada."""
    subredes_info = []
    subredes = ec2.describe_subnets()['Subnets']

    # Obtener tablas de rutas para identificar subredes públicas
    route_tables = ec2.describe_route_tables()['RouteTables']
    public_subnet_ids = set()

    for rt in route_tables:
        for association in rt.get('Associations', []):
            for route in rt.get('Routes', []):
                if route.get('GatewayId', '').startswith('igw-'):
                    public_subnet_ids.add(association.get('SubnetId'))

    for subnet in subredes:
        tags = ", ".join([f"{t['Key']}={t['Value']}" for t in subnet.get('Tags', [])])
        subnet_type = 'Pública' if subnet['SubnetId'] in public_subnet_ids else 'Privada'
        
        subredes_info.append({
            'Subnet ID': subnet['SubnetId'],
            'VPC ID': subnet['VpcId'],
            'CIDR': subnet['CidrBlock'],
            'AZ': subnet['AvailabilityZone'],
            'Tipo': subnet_type,
            'Tags': tags if tags else "Sin etiquetas"
        })
    return subredes_info