terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "KPMG21_RobertaDomanico_ProjectExercise"
    storage_account_name = "rubystorage1985"
    container_name       = "rubystorage1985"
    key                  = "state.tfstate"
  }
}

resource "azurerm_storage_account" "tfstate" {
  name                     = "rubystorage1985"
  resource_group_name      = data.azurerm_resource_group.main.name
  location                 = data.azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "rubystorage1985"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "blob"
}
provider "azurerm" {
  features {}
}
data "azurerm_resource_group" "main" {
  name = "KPMG21_RobertaDomanico_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "rubyappserviceplan-${var.prefix}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}



resource "azurerm_cosmosdb_account" "rubycosmos" {
  name                 = "rubycosmos-${var.prefix}"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = 4.2

  enable_automatic_failover = true


  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }


  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }


}
resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "databaseruby"
  resource_group_name = azurerm_cosmosdb_account.rubycosmos.resource_group_name
  account_name        = azurerm_cosmosdb_account.rubycosmos.name
  # lifecycle { prevent_destroy = true }
}

resource "azurerm_linux_web_app" "main" {
  name                = "rubyapp1985-${var.prefix}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id


  site_config {
    application_stack {
      docker_image     = "rubydoma/todo-app-exercise-8"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "CONNECTION_STRING"                   = azurerm_cosmosdb_account.rubycosmos.connection_strings[0]
    "COLLECTION_NAME"                     = "collectionruby"
    "COSMOSODB_NAME"                      = "rubycosmos"
    "CLIENT_ID"                           = var.clientid
    "CLIENT_SECRET"                       = var.clientsecret
    "FLAS_APP"                            = "todo_app/app"
    "FLASK_ENV"                           = "development"
    "SECRET_KEY"                          = "notused"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://rubydoma"
    "LOG_LEVEL"                           = "DEBUG"
    "LOGGLY_TOKEN"                        = var.loggly_token
  }

}