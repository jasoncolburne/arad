vault {
  enabled = true
  address = "http://localhost:8200"
}

plugin "docker" {
  config {
    volumes {
      enabled = true
    }
  }
}

