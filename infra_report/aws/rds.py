# aws/rds.py
def obtener_rds(rds):
    """Obtiene información de instancias RDS."""
    rds_info = []
    instances = rds.describe_db_instances()['DBInstances']
    for instance in instances:
        grupos_seguridad = [sg['VpcSecurityGroupId'] for sg in instance['VpcSecurityGroups']]
        rds_info.append({
            'DB Identifier': instance['DBInstanceIdentifier'],
            'Engine': instance['Engine'],
            'Status': instance['DBInstanceStatus'],
            'Endpoint': instance['Endpoint']['Address'],
            'VPC': instance['DBSubnetGroup']['VpcId'],
            'Security Groups': ', '.join(grupos_seguridad)
        })
    return rds_info
