plugin "docker" {
  config {
    cni_path = "/home/jason/src/cni-plugins/bin:/home/jason/go/bin"
    volumes {
      enabled = true
    }
  }
}

