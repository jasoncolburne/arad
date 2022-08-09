client {
  cni_path = "/home/jason/src/cni-plugins/bin"
}

plugin "docker" {
  config {
    volumes {
      enabled = true
    }
  }
}

