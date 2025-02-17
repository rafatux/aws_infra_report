def obtener_load_balancers(elbv2):
    """Obtiene información de Load Balancers (ALB/ELB)."""
    alb_info = []
    lbs = elbv2.describe_load_balancers()['LoadBalancers']
    for lb in lbs:
        alb_info.append({
            'Name': lb['LoadBalancerName'],
            'Type': lb['Type'],
            'DNS Name': lb['DNSName'],
            'Scheme': lb['Scheme'],
            'VPC ID': lb['VpcId'],
            'Public IP': 'Sí' if lb['Scheme'] == 'internet-facing' else 'No'
        })
    return alb_info

def obtener_target_groups(elbv2):
    """Obtiene información de Target Groups."""
    tg_info = []
    tgs = elbv2.describe_target_groups()['TargetGroups']
    for tg in tgs:
        tg_info.append({
            'Target Group Name': tg['TargetGroupName'],
            'Protocol': tg['Protocol'],
            'Port': tg['Port'],
            'VPC ID': tg['VpcId']
        })
    return tg_info