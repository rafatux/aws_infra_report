def obtener_ecs(ecs):
    """Obtiene información de tareas y contenedores ECS."""
    ecs_info = []
    clusters = ecs.list_clusters()['clusterArns']
    for cluster_arn in clusters:
        tasks = ecs.list_tasks(cluster=cluster_arn)['taskArns']
        for task_arn in tasks:
            task_details = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])['tasks'][0]
            container_instance_arn = task_details.get('containerInstanceArn', 'N/A')
            launch_type = task_details.get('launchType', 'Desconocido')
            ecs_info.append({
                'Cluster': cluster_arn.split('/')[-1],
                'Task ARN': task_arn,
                'Container Instance ARN': container_instance_arn,
                'Launch Type': launch_type
            })
    return ecs_info