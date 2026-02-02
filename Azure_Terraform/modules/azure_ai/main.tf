resource "azurerm_cognitive_account" "azure_ai" {
  name                = var.ai_name
  location            = var.default_loc
  resource_group_name = var.default_rg

  kind     = "CognitiveServices"
  sku_name = var.ai_sku
}
