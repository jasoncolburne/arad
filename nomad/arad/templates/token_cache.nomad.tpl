job "token_cache" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this cache, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "token_cache" {
    count = 1

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name     = "token-cache"
      port     = "6379"
      provider = "consul"
      connect {
        sidecar_service {}
      }
    }

    task "redis" {
      driver = "docker"

      config {
        image          = "redis:bullseye"
        auth_soft_fail = true
      }

      [[ template "resources" .arad.token_cache_resources -]]
    }
  }
}
