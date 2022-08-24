job "reader_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reader_service" {
    count = [[ .arad.reader_service_count ]]

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name     = "reader-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.reader-remove-prefix.stripprefix.prefixes=/api/v1/read",
        "api.http.middlewares.reader-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.reader.tls=true",
        "api.http.routers.reader.entrypoints=https",
        "api.http.routers.reader.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/read/`)",
        "api.http.routers.reader.middlewares=reader-remove-prefix@consulcatalog"
      ]

      connect {
        sidecar_service {
          proxy {
            config {
              protocol = "tcp"
              mode = "transparent"
            }
            upstreams {
              destination_name = "application-database"
              local_bind_port  = 5432
              mesh_gateway {
                mode = "local"
              }
            }
          }
        }
      }

      check {
        name = "alive"
        type = "http"
        port = "80"
        path = "/health"
        interval = "5s"
        timeout = "1s"
        address_mode = "driver"
      }
    }

    task "fastapi" {
      driver = "docker"

      vault {
        policies = ["kv"]
      }

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image = [[ .arad.reader_service_image | quote ]]
      }

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
        LISTEN_IP = "127.0.0.1"
      }

      template {
        data = <<EOH
DATABASE_URL="{{ with secret "kv/data/application_database_url" }}{{ .Data.data.value }}{{ end }}"
EOH
        destination = "secrets/.env"
        env = true
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
