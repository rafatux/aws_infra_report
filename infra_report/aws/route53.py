# aws/route53.py

import boto3

def obtener_zonas_dns_y_registros(route53_client):
    """Obtiene información de las zonas DNS de Route 53 y sus registros."""
    zonas_info = []
    response = route53_client.list_hosted_zones()

    for zone in response['HostedZones']:
        zone_id = zone['Id'].split('/')[-1]
        registros = obtener_registros_dns(route53_client, zone_id)
        zonas_info.append({
            'Zone ID': zone_id,
            'Nombre': zone['Name'],
            'Pública': 'Sí' if not zone['Config'].get('PrivateZone', False) else 'No',
            'Comentario': zone['Config'].get('Comment', 'N/A'),
            'Cantidad de Registros': len(registros),
            'Registros': registros
        })

    return zonas_info

def obtener_registros_dns(route53_client, zone_id):
    """Obtiene los registros DNS de una zona hospedada específica."""
    registros = []
    paginator = route53_client.get_paginator('list_resource_record_sets')
    for page in paginator.paginate(HostedZoneId=zone_id):
        for record_set in page['ResourceRecordSets']:
            registros.append({
                'Nombre': record_set['Name'],
                'Tipo': record_set['Type'],
                'TTL': record_set.get('TTL', 'N/A'),
                'Valores': [r['Value'] for r in record_set.get('ResourceRecords', [])]
            })
    return registros
