# 📊 Proyecto: Informe de Infraestructura AWS

## 📝 Descripción
Este proyecto genera un **informe completo de la infraestructura AWS** en formato Markdown (`.md`) y un **esquema visual** (`.png`) de las relaciones entre recursos.

**Recursos que analiza:**
- 🟡 **VPCs, Subredes y EC2**
- 🟠 **Load Balancers (ALB/ELB) y Target Groups**
- 🟢 **ECS (Clusters y Tareas)**
- 🟣 **IAM (Roles, Políticas y Statements)**
- 🔵 **RDS (Bases de datos)**
- 🟤 **S3 (Buckets)**
- 🟠 **Lambdas (Funciones)**

También genera un **esquema visual** de las relaciones entre recursos usando `Graphviz`.

---

## 🛠️ Instalación

### 1️⃣ **Clonar el Repositorio:**
```bash
git clone https://github.com/tuusuario/infra_report.git
cd infra_report
```

### 2️⃣ **Instalar Python y Poetry:**
- Asegúrate de tener **Python 3.13** y **Poetry** instalado.

```bash
brew install poetry
poetry --version  # Verificar instalación
```

### 3️⃣ **Instalar Dependencias:**
```bash
poetry install
```

---

## 🚀 Uso

### ✅ **Generar el Informe:**
```bash
poetry run infra-report --profile dev --output informe_aws.md --graph aws_infra
```
- `--profile`: Perfil de AWS configurado.
- `--output`: Nombre del archivo de informe.

### 📂 **Archivos Generados:**
- 📄 `informe_aws.md` → Informe completo.

---

## ⚙️ Estructura del Proyecto
```plaintext
infra_report/
└── infra_report/
    ├── main.py           # Punto de entrada principal
    ├── aws/              # Módulos AWS
    │   ├── ec2.py        # VPC, Subredes, EC2
    │   ├── elb.py        # Load Balancers y Target Groups
    │   ├── ecs.py        # ECS Clusters y Tareas
    │   ├── iam.py        # IAM Policies y Roles
    │   ├── rds.py        # RDS Instances
    │   ├── s3.py         # S3 Buckets
    │   ├── gateway.py    # gateway info
    │   ├── rds.py        # rds instances
    │   ├── route53.py    # Rote53 registros
    │   └── lambda_.py    # Lambda Functions
    └── utils/            # Utilidades
        ├── markdown.py   # Formato Markdown
        └── helpers.py    # Funciones auxiliares
```

---

## 🛡️ Requisitos AWS
- Tener configurado un perfil en `~/.aws/credentials`.
- Permisos para acceder a EC2, ELB, ECS, RDS, IAM, S3 y Lambda.

---

## 🧪 Comandos Útiles
- **Formatear código:** `poetry run black .`
- **Verificar errores:** `poetry run flake8 .`
- **Ejecutar pruebas:** `poetry run pytest`

---

## 👥 Colaboradores
- Rafael Fernandez (@rafaelfernandez)
---

## 📝 Licencia
Este proyecto se distribuye bajo la licencia **GNU AFFERO GENERAL PUBLIC LICENSE**.

