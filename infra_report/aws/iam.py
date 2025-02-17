def obtener_iam_policies(iam):
    """Obtiene políticas IAM (con Statements JSON)."""
    policies_info = []
    policies = iam.list_policies(Scope='Local')['Policies']
    for policy in policies:
        policy_version = iam.get_policy_version(
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId']
        )
        document = policy_version['PolicyVersion']['Document']
        policies_info.append({
            'Policy Name': policy['PolicyName'],
            'Arn': policy['Arn'],
            'Document': document
        })
    return policies_info

def obtener_roles_y_policies(iam):
    """Obtiene roles IAM y sus políticas asociadas."""
    roles_info = []
    roles = iam.list_roles()['Roles']
    for role in roles:
        attached_policies = iam.list_attached_role_policies(RoleName=role['RoleName'])['AttachedPolicies']
        inline_policies = iam.list_role_policies(RoleName=role['RoleName'])
        roles_info.append({
            'Role Name': role['RoleName'],
            'Attached Policies': [p['PolicyName'] for p in attached_policies],
            'Inline Policies': inline_policies['PolicyNames']
        })
    return roles_info