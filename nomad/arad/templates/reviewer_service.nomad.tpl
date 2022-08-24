job "reviewer_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reviewer_service" {
    count = [[ .arad.reviewer_service_count ]]

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name = "reviewer-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.reviewer-remove-prefix.stripprefix.prefixes=/api/v1/review",
        "api.http.middlewares.reviewer-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.reviewer.tls=true",
        "api.http.routers.reviewer.entrypoints=https",
        "api.http.routers.reviewer.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/review/`)",
        "api.http.routers.reviewer.middlewares=reviewer-remove-prefix@consulcatalog"
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
        image = [[ .arad.reviewer_service_image | quote ]]
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
