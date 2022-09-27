
from email.mime import base
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient


config = {
    'inputs': [
        {
          'data_product_id': 'get id from data product registry',
          'user_id': 'Service Principal ID'
        }
    ],
    'source-system': {
        'storage-account-url': 'https://datalake9n8.dfs.core.windows.net/',
        'name': 'SHARKdata',
        'entities': [
            {
                'name': 'bacterioplankton',
                'version': '1.0.0',
                'access': 'setup ACL for this entity - should manage ',
                'primary_key': ['column_name'],
                'partition_by': 'column_name'
            },
            {
                'name': 'zooplankton',
                'version': '1.0.0',
                'access': 'setup ACL for this entity - should manage ',
                'primary_key': ['column_name'],
                'partition_by': 'column_name'
            }
        ]
    },
    'data-products': [
        {
            'storage-account-url': 'https://datalake9n8.dfs.core.windows.net/',
            'name': 'bacterioplankton',
            'access': 'ad-group',
            'entities': [
                {
                    'name': 'monthly-occurance',
                    'version': '1.0.0'
                }
            ]
        },
        {
            'storage-account-url': 'https://datalake9n8.dfs.core.windows.net/',
            'name': 'zooplankton',
            'access': 'ad-group',
            'entities': [
                {
                    'name': 'monthly-occurance',
                    'version': '1.0.0'
                }
            ]
        }
    ]

}

containers = {
    'entity_containers': [
        {
            'name': 'raw-landing',
            'layout': [
                'delta',
                'full'
            ]
        },
        {
            'name': 'raw-conformed',
            'layout': [
                'delta/input',
                'delta/output',
                'delta/error',
                'full/input',
                'full/output',
                'full/error',

            ]
        },
        {
            'name': 'standardized',
            'layout': [
                'general',
                'sensitive'
            ]
        }
    ],
    'data_products_container': {
        'name': 'data-products',
        'layout': [
            'general',
            'sensitive'
        ]
    }
}

def setup_source_system(src_system_conf, containers):
    create_entity_containers(src_system_conf, containers['entity_containers'])

def create_entity_containers(src_system_conf, entity_containers):
    for container in entity_containers:
        file_system_client = get_file_system_client(src_system_conf['storage-account-url'], container['name'])
        base_dir = f'source-system={src_system_conf["name"]}'
        file_system_client.create_directory(base_dir)
        create_entity_dirs(file_system_client, base_dir, src_system_conf['entities'], container['layout'])

def setup_data_products(data_products_conf, data_product_container):
    for data_product in data_products_conf:
        file_system_client = get_file_system_client(data_product['storage-account-url'], data_product_container['name'])
        base_dir = f'data-product={data_product["name"]}'
        file_system_client.create_directory(base_dir)
        create_entity_dirs(file_system_client, base_dir, data_product['entities'], data_product_container['layout'])

def get_file_system_client(dfs_account_url, file_system):
    dl_service_client = DataLakeServiceClient(dfs_account_url, credential=DefaultAzureCredential())
    file_system_client = dl_service_client.get_file_system_client(file_system=file_system)
    
    return file_system_client

def create_entity_dirs(file_system_client, base_dir, entities, layout):
    for entity in entities:
        for sub_dir in layout:
            entityDir = f'{base_dir}/entity={entity["name"]}/version={entity["version"]}/{sub_dir}'
            file_system_client.create_directory(entityDir)


if __name__ == "__main__":
    setup_source_system(config['source-system'], containers)
    setup_data_products(config['data-products'], containers['data_products_container'])
