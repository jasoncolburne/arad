vault {
  enabled = true
  address = "https://localhost:8200"
}

plugin "docker" {
  config {
    volumes {
      enabled = true
    }
  }
}

