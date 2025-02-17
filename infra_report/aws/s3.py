# aws/s3.py
import json
from botocore.exceptions import ClientError

def obtener_buckets_s3(s3):
    """Obtiene información detallada de los buckets S3, incluyendo políticas y configuraciones de ciclo de vida."""
    bucket_info = []

    try:
        buckets = s3.list_buckets()['Buckets']
        for bucket in buckets:
            bucket_name = bucket['Name']
            region = s3.get_bucket_location(Bucket=bucket_name).get('LocationConstraint', 'us-east-1')

            # Obtener la política del bucket
            try:
                policy = s3.get_bucket_policy(Bucket=bucket_name)
                policy_json = json.loads(policy['Policy'])
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                    policy_json = None
                else:
                    print(f"Error al obtener la política del bucket {bucket_name}: {e}")
                    policy_json = None

            # Obtener la configuración de ciclo de vida del bucket
            try:
                lifecycle = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                lifecycle_rules = lifecycle['Rules']
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    lifecycle_rules = None
                else:
                    print(f"Error al obtener la configuración de ciclo de vida del bucket {bucket_name}: {e}")
                    lifecycle_rules = None

            bucket_info.append({
                'Bucket Name': bucket_name,
                'Region': region,
                'Creation Date': bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S'),
                'Policy': policy_json,
                'Lifecycle Configuration': lifecycle_rules
            })
    except ClientError as e:
        print(f"Error al obtener información de los buckets: {e}")
        return []

    return bucket_info
