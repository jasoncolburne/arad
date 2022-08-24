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

    # https://medium.com/hashicorp-engineering/the-trouble-with-service-mesh-6b0336964323
    service {
      name        = "token-cache"
      socket_path = "/var/run/redis/socket"
      provider    = "consul"
      connect {
        sidecar_service {}
      }
      check {
        name = "ping"
        task = "redis"
        type = "script"
        command = "/usr/local/bin/redis-cli"
        args = ["-s", "/var/run/redis/socket", "PING"]
        interval = "5s"
        timeout = "1s"
      }
    }

    task "redis" {
      driver = "docker"

      config {
        image          = [[ .arad.token_cache_image | quote ]]
        auth_soft_fail = true
      }

      [[ template "resources" .arad.token_cache_resources -]]
    }
  }
}
