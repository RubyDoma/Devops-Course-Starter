terraform {
required_providers {
azurerm = {
source = "hashicorp/azurerm"
version = ">= 3.8"
}
}
}
provider "azurerm" {
features {}
}
data "azurerm_resource_group" "main" {
name = "KPMG21_RobertaDomanico_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
name = "terraformed-asp"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type = "Linux"
sku_name = "B1"
}
resource "azurerm_linux_web_app" "main" {
name = "apprubydoma"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id = azurerm_service_plan.main.id
  
  site_config {
    application_stack {
      docker_image = "appsvcsample/python-helloworld"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "KPMG21_RobertaDomanico_ProjectExercise"
  location = "UK South"
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}



resource "azurerm_cosmosdb_account" "ruby-cosmos-account" {
  name                = "tfex-cosmos-db-${random_integer.ri.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities { 
    name = "EnableServerless" 
    }

capabilities { 
    name = "EnableMongo" 
}
lifecycle { prevent_destroy = true }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "eastus"
    failover_priority = 1
  }

  geo_location {
    location          = "westus"
    failover_priority = 0
  }

  
}

data "azurerm_cosmosdb_account" "main" {
  name                = "ruby-cosmos-account"
  resource_group_name = "KPMG21_RobertaDomanico_ProjectExercise"
 
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "ruby-database"
  resource_group_name = data.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.main.name
  throughput          = 400
}

resource "azurerm_app_service" "main" {
  name                = "ruby-webapp"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id


  site_config {
    dotnet_framework_version = "v4.0"
    scm_type                 = "LocalGit"
  }

  app_settings = {
    "MONGODB_CONNECTION_STRING" = azurerm_cosmosdb_account.main.connection_strings[0],
    "COLLECTION_NAME" =  azurerm_cosmosdb_account.main.collection_name,
    "RUBY_KEY" = azurerm_cosmosdb_account.main.RUBY_KEY,
    "RUBY_TOKEN" = azurerm_cosmosdb_account.main.RUBY_TOKEN,
    "BOARD_ID" = azurerm_cosmosdb_account.main.BOARD_ID,
    "TO_DO_ID" = azurerm_cosmosdb_account.main.TO_DO_ID,
    "DOING_ID" = azurerm_cosmosdb_account.main.DOING_ID,
    "DONE_ID" = azurerm_cosmosdb_account.main.DONE_ID,
    "COSMOSODB_NAME"= azurerm_cosmosdb_account.main.COSMOSODB_NAME,
    "CLIENT_ID"= azurerm_cosmosdb_account.main.CLIENT_ID,
    "CLIENT_SECRET"= azurerm_cosmosdb_account.main.CLIENT_SECRET,
    "FLAS_APP" = azurerm_cosmosdb_account.main.FLAS_APP,
    "FLASK_ENV" =  azurerm_cosmosdb_account.main.FLASK_ENV,
    "SECRET_KEY" =  azurerm_cosmosdb_account.main.SECRET_KEY
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = False,
     "DOCKER_REGISTRY_SERVER_URL" = azurerm_cosmosdb_account.main.DOCKER_REGISTRY_SERVER_URL
  }

}