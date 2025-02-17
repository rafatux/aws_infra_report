# utils/helpers.py
from .markdown import dict_to_markdown_table, statements_to_markdown
from datetime import datetime

def dict_to_markdown_table(data, headers):
    """Convierte una lista de diccionarios en una tabla Markdown."""
    if not data:
        return "No hay datos disponibles.\n"

    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(['---'] * len(headers)) + " |\n"

    for item in data:
        row = [str(item.get(header, '')) for header in headers]
        table += "| " + " | ".join(row) + " |\n"

    return table

def generar_informe_markdown(
    vpcs, subredes, ec2_instances, alb, tgs, ecs_tasks,
    iam_policies, iam_roles,
    rds_instances, s3_buckets, lambdas,
    zonas_dns, gateways,
    output_file
):
    """Genera el informe completo en formato Markdown."""
    with open(output_file, 'w') as f:
        f.write(f"---\n")
        f.write(f"title: 'Informe de Infraestructura AWS'\n")
        f.write(f"date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n")
        f.write(f"author: \"Sistema de Informes\"\n")
        f.write(f"---\n\n")

        f.write(f"# 📊 Informe de Infraestructura AWS\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # ✅ VPCs
        f.write("## 🟡 VPCs\n")
        headers = ["VPC ID", "CIDR", "Estado"]
        f.write(dict_to_markdown_table(vpcs, headers))
        f.write("\n")

        # ✅ Subredes
        f.write("## 🟠 Subredes (Públicas y Privadas, con Tags)\n")
        headers = ["Subnet ID", "VPC ID", "CIDR", "AZ", "Tipo", "Tags"]
        f.write(dict_to_markdown_table(subredes, headers))
        f.write("\n")

        # ✅ EC2 Instances
        f.write("## 🟢 Instancias EC2\n")
        headers = ["Instance ID", "State", "Type", "Public IP", "Private IP", "AZ"]
        f.write(dict_to_markdown_table(ec2_instances, headers))
        f.write("\n")

        # ✅ Load Balancers (ALB/ELB)
        f.write("## 🟣 Load Balancers (ALB/ELB)\n")
        headers = ["Name", "Type", "DNS Name", "Scheme", "VPC ID", "Public IP"]
        f.write(dict_to_markdown_table(alb, headers))
        f.write("\n")

        # ✅ Target Groups
        f.write("## 🟤 Target Groups\n")
        headers = ["Target Group Name", "Protocol", "Port", "VPC ID"]
        f.write(dict_to_markdown_table(tgs, headers))
        f.write("\n")

        # ✅ ECS Tasks
        f.write("## 🟡 Tareas y Contenedores ECS\n")
        headers = ["Cluster", "Task ARN", "Container Instance ARN", "Launch Type"]
        f.write(dict_to_markdown_table(ecs_tasks, headers))
        f.write("\n")

        # ✅ IAM Policies
        f.write("## 🟠 Políticas IAM (con Statements detallados)\n")
        for policy in iam_policies:
            f.write(f"### {policy['Policy Name']}\n")
            f.write(f"**ARN:** `{policy['Arn']}`\n\n")
            f.write("**Statements:**\n")
            f.write(statements_to_markdown(policy['Document'].get('Statement', [])))
            f.write("\n---\n")
        f.write("\n")

        # ✅ IAM Roles
        f.write("## 🟣 Roles IAM y Políticas Asociadas\n")
        headers = ["Role Name", "Attached Policies", "Inline Policies"]
        f.write(dict_to_markdown_table(iam_roles, headers))
        f.write("\n")

        # ✅ RDS Instances
        f.write("## 🔵 RDS Instances\n")
        headers = ["DB Identifier", "Engine", "Status", "Endpoint", "VPC"]
        f.write(dict_to_markdown_table(rds_instances, headers))
        f.write("\n")

        # ✅ S3 Buckets
        f.write("## 🟤 S3 Buckets\n")
        headers = ["Bucket Name", "Region", "Creation Date"]
        f.write(dict_to_markdown_table(s3_buckets, headers))
        f.write("\n")

        # ✅ Lambda Functions
        f.write("## 🟠 Lambda Functions\n")
        headers = ["Function Name", "Runtime", "Role", "Last Modified"]
        f.write(dict_to_markdown_table(lambdas, headers))
        f.write("\n")
        
        if zonas_dns:
            f.write("## 🟢 Zonas DNS (Route 53)\n")
            headers = ["Zone ID", "Nombre", "Pública", "Comentario", "Cantidad de Registros"]
            f.write(dict_to_markdown_table(zonas_dns, headers))
            f.write("\n")

            # Detalle de Registros DNS por Zona
            for zona in zonas_dns:
                f.write(f"### Detalles de la Zona: {zona['Nombre']}\n")
                registros = zona['Registros']
                if registros:
                    headers = ["Nombre", "Tipo", "TTL", "Valores"]
                    f.write(dict_to_markdown_table(registros, headers))
                else:
                    f.write("No se encontraron registros DNS en esta zona.\n")
                f.write("\n")

        # 🟣 Gateways (Internet y NAT)
        if gateways:
            f.write("## 🟣 Gateways (Internet y NAT)\n")
            headers = ["Gateway Type", "Gateway ID", "VPC ID", "Subnet ID", "Estado", "IP Pública"]
            f.write(dict_to_markdown_table(gateways, headers))
            f.write("\n")

    print(f"✅ Informe generado: {output_file}")
    