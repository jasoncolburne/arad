job "token_cache" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "token_cache" {
    count = 1

    network {
      mode = [[ .arad.network_mode ]]
    }

    service {
      name     = "token-cache"
      port     = "6379"
      provider = "consul"

      connect {
        sidecar_service {}
      }

      check {
        name = "ping"
        task = "redis"
        type = "script"
        command = "/usr/local/bin/redis-cli"
        args = ["PING"]
        interval = "5s"
        timeout = "1s"

        [[ template "check_restart" . ]]
      }
    }

    task "redis" {
      driver = "docker"

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        image          = "redis:bullseye"
        auth_soft_fail = true
      }

      [[ template "resources" .arad.token_cache_resources -]]
    }
  }
}
