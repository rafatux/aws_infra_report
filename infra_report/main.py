# infra_report/main.py
import argparse
import boto3

# infra_report/main.py
from .aws.ec2 import obtener_vpcs, obtener_subredes, obtener_ec2
from .aws.elb import obtener_load_balancers, obtener_target_groups
from .aws.ecs import obtener_ecs
from .aws.iam import obtener_iam_policies, obtener_roles_y_policies
from .aws.rds import obtener_rds
from .aws.s3 import obtener_buckets_s3
from .aws.lambda_ import obtener_lambdas
from .aws.route53 import obtener_zonas_dns_y_registros
from .aws.gateway import obtener_gateways


from .utils.helpers import generar_informe_markdown
from .utils.graph import generar_grafo_recursos


def main():
    parser = argparse.ArgumentParser(description='Generar informe de infraestructura AWS.')
    parser.add_argument('--profile', required=True, help='Perfil de AWS configurado en ~/.aws/credentials')
    parser.add_argument('--output', default='informe_aws.md', help='Archivo de salida (Markdown)')
    parser.add_argument('--graph', default='aws_infra', help='Archivo de esquema visual (sin extensión)')
    args = parser.parse_args()

    # Crear sesión AWS
    session = boto3.Session(profile_name=args.profile)
    ec2 = session.client('ec2')
    elbv2 = session.client('elbv2')
    ecs = session.client('ecs')
    iam = session.client('iam')
    rds = session.client('rds')
    s3 = session.client('s3')
    route53 = session.client('route53')
    lambda_client = session.client('lambda')

    # Obtener datos
    vpcs = obtener_vpcs(ec2)
    subredes = obtener_subredes(ec2)
    ec2_instances = obtener_ec2(ec2)
    alb = obtener_load_balancers(elbv2)
    tgs = obtener_target_groups(elbv2)
    ecs_tasks = obtener_ecs(ecs)
    iam_policies = obtener_iam_policies(iam)
    iam_roles = obtener_roles_y_policies(iam)
    rds_instances = obtener_rds(rds)
    s3_buckets = obtener_buckets_s3(s3)
    lambdas = obtener_lambdas(lambda_client)
    zonas_dns = obtener_zonas_dns_y_registros(route53)
    gateways = obtener_gateways(ec2)

    # Generar informe Markdown
    generar_informe_markdown(
        vpcs, subredes, ec2_instances, alb, tgs, ecs_tasks,
        iam_policies, iam_roles, rds_instances, s3_buckets,
        lambdas, zonas_dns, gateways, args.output
    )

    # Generar esquema visual
    # generar_grafo_recursos(
    #     ec2_instances, s3_buckets, lambdas, rds_instances, args.graph
    # )

if __name__ == '__main__':
    main()
