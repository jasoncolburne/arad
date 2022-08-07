job "token_cache" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this cache, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "token_cache" {
    count = 1

    network {
      port "db" {
        to = [[ .arad.token_cache_port ]]
      }
    }

    task "redis" {
      driver = "docker"

      config {
        image          = "redis:bullseye"
        ports          = ["db"]
        auth_soft_fail = true
      }

      service {
        name     = "token-cache"
        provider = "nomad"
        port     = "db"
      }

      [[ template "resources" .arad.token_cache_resources -]]
    }
  }
}
