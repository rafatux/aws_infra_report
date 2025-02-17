# ===========================================
# Funciones para el formato Markdown
# ===========================================
import json

def dict_to_markdown_table(data_list, headers):
    """Convierte una lista de diccionarios en tabla Markdown."""
    if not data_list:
        return "No hay datos disponibles.\n"
    
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["-" * len(h) for h in headers]) + " |\n"
    
    for item in data_list:
        row = "| " + " | ".join([str(item.get(h, 'N/A'))[:150] for h in headers]) + " |\n"
        table += row
    return table

def format_statement_value(value):
    """Formatea el valor de una declaración IAM para Markdown."""
    if isinstance(value, list):
        return ", ".join(value)
    elif isinstance(value, dict):
        return json.dumps(value, indent=2)  # Muestra JSON formateado
    return str(value)

def statements_to_markdown(statements):
    """Formatea los 'Statements' de políticas IAM en tabla Markdown."""
    if not statements:
        return "No hay declaraciones ('Statements').\n"
    
    markdown = "| Acción | Efecto | Recurso |\n"
    markdown += "|--------|--------|---------|\n"
    
    for stmt in statements:
        actions = format_statement_value(stmt.get('Action', 'N/A'))
        effect = stmt.get('Effect', 'N/A')
        resources = format_statement_value(stmt.get('Resource', 'N/A'))
        
        markdown += f"| `{actions}` | `{effect}` | `{resources}` |\n"
    return markdown