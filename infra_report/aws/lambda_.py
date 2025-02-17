# aws/lambda_.py
def obtener_lambdas(lambda_client):
    """Obtiene información de funciones Lambda."""
    lambda_info = []
    functions = lambda_client.list_functions()['Functions']
    for function in functions:
        lambda_info.append({
            'Function Name': function['FunctionName'],
            'Runtime': function['Runtime'],
            'Role': function['Role'],
            'Last Modified': function['LastModified']
        })
    return lambda_info
