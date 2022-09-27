# Data Platform

Storage: ADLS Gen2
Orchestrator: ADF
Compute: Databricks

Pipeline:
1. Landing: raw-landing
2. Ingest: raw-conformed
3. Clean: standardized
4. Aggregate: data-products

## Setup

### Azure CLI
https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

### Python
```
python3.9 -m venv env  
source env/bin/activate
pip install -r requirements.txt
```
### Terraform
https://www.terraform.io/downloads


```
# Configure Service Principal for terraform deployments
az login
az account set --subscription "2dabeea8-262c-4673-803b-139802c3b2b6"
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/2dabeea8-262c-4673-803b-139802c3b2b6"
```


## Infra

### Storage
python storage/storage.py

