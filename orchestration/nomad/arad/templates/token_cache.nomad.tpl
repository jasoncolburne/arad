job "token_cache" {
  type = "service"

  [[ template "region" . ]]

  datacenters = ["dc1"]

  group "token_cache" {
    count = 1

    network {
      mode = [[ .arad.network_mode | quote ]]
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

        command = "redis-server"
        args = [
          "/etc/redis/redis.conf",
        ]

        mount {
          type = "volume"
          target = "/bitnami/redis/data"
          source = "arad_token_cache"
          readonly = false
        }

        mount {
          type = "bind"
          target = "/etc/redis/redis.conf"
          source = "local/redis.conf"
          readonly = true
        }
      }

      template {
        data = <<EOF
bind 127.0.0.1
EOF

        change_mode = "restart"
        destination = "local/redis.conf"
      }

      [[ template "resources" .arad.token_cache_resources ]]
    }
  }
}
