locals {
  frontend_code_blob_url = "https://${var.sa_name}.blob.core.windows.net/${var.code_container}/frontend/${var.frontend_code}"
  backend_code_blob_url  = "https://${var.sa_name}.blob.core.windows.net/${var.code_container}/backend/${var.backend_code}"
}
