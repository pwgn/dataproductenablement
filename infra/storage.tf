resource "azurerm_storage_account" "data_lake" {
    name                        = format("%s%s", "datalake", random_id.st.id)
    resource_group_name         = azurerm_resource_group.rg.name
    location                    = azurerm_resource_group.rg.location
    account_kind                = "StorageV2"
    account_tier                = "Standard"
    account_replication_type    = "LRS"
    enable_https_traffic_only   = true
    min_tls_version             = "TLS1_2"
    is_hns_enabled              = true
    public_network_access_enabled = true 
    #infrastructure_encryption_enabled = true
}

resource "azurerm_storage_container" "raw_landing" {
    name = "raw-landing"
    storage_account_name = azurerm_storage_account.data_lake.name
    container_access_type = "private"
}

resource "azurerm_storage_container" "raw_conformed" {
    name = "raw-conformed"
    storage_account_name = azurerm_storage_account.data_lake.name
    container_access_type = "private"
}

resource "azurerm_storage_container" "standardized" {
    name = "standardized"
    storage_account_name = azurerm_storage_account.data_lake.name
    container_access_type = "private"
}

resource "azurerm_storage_container" "data_products" {
    name = "data-products"
    storage_account_name = azurerm_storage_account.data_lake.name
    container_access_type = "private"
}
