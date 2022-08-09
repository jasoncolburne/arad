cni_path = "/home/jason/src/cni-plugins/bin:/home/jason/go/bin"

plugin "docker" {
  config {
    volumes {
      enabled = true
    }
  }
}

