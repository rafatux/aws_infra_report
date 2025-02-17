# utils/graph.py
#from graphviz import Digraph

def generar_grafo_recursos(ec2_instances, s3_buckets, lambdas, rds_instances, output_file):
    """Genera un gráfico de relaciones de infraestructura AWS (orientación vertical)."""
    dot = Digraph(comment='AWS Infrastructure')

    # 📌 Ajustes Generales: Orientación Vertical y Espaciado
    dot.attr(rankdir='TB', size='10,15!', nodesep='0.6', ranksep='1.5', overlap='false', fontsize='12')

    # 🟡 Cluster: EC2
    with dot.subgraph(name='cluster_ec2') as c:
        c.attr(label='EC2 Instances', style='dashed', color='blue')
        for ec2 in ec2_instances:
            c.node(ec2['Instance ID'], f"💻 EC2\n{ec2['Instance ID']}\n{ec2['Type']}", shape='box', style='filled', fillcolor='lightblue')

    # 🟢 Cluster: RDS
    with dot.subgraph(name='cluster_rds') as c:
        c.attr(label='RDS Instances', style='dashed', color='green')
        for rds in rds_instances:
            c.node(rds['DB Identifier'], f"🗄️ RDS\n{rds['DB Identifier']}\n{rds['Engine']}", shape='cylinder', style='filled', fillcolor='lightgreen')

    # 🟤 Cluster: S3
    with dot.subgraph(name='cluster_s3') as c:
        c.attr(label='S3 Buckets', style='dashed', color='brown')
        for bucket in s3_buckets:
            c.node(bucket['Bucket Name'], f"🪣 S3\n{bucket['Bucket Name']}", shape='folder', style='filled', fillcolor='tan')

    # 🟠 Cluster: Lambda
    with dot.subgraph(name='cluster_lambda') as c:
        c.attr(label='Lambda Functions', style='dashed', color='orange')
        for function in lambdas:
            c.node(function['Function Name'], f"⚙️ Lambda\n{function['Function Name']}", shape='ellipse', style='filled', fillcolor='gold')

    # ➡️ Relacionar Recursos Verticalmente
    for ec2 in ec2_instances:
        for bucket in s3_buckets:
            dot.edge(ec2['Instance ID'], bucket['Bucket Name'], label="S3:Read/Write", style="dashed")
        for rds in rds_instances:
            dot.edge(ec2['Instance ID'], rds['DB Identifier'], label="RDS:Connect", color="green")

    for function in lambdas:
        for bucket in s3_buckets:
            dot.edge(function['Function Name'], bucket['Bucket Name'], label="S3:PutObject", color="brown")

    # Guardar el gráfico
    dot.render(output_file, format='png', cleanup=True)
    print(f"✅ Esquema visual generado (vertical): {output_file}.png")
