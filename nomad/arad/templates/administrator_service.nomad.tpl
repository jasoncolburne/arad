job "administrator_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "administrator_service" {
    count = [[ .arad.administrator_service_count ]]

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name = "administrator-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.administrator-remove-prefix.stripprefix.prefixes=/api/v1/administrate",
        "api.http.middlewares.administrator-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.administrator.tls=true",
        "api.http.routers.administrator.entrypoints=https",
        "api.http.routers.administrator.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/administrate/`)",
        "api.http.routers.administrator.middlewares=administrator-remove-prefix@consulcatalog"
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

      [[ template "service_health_check" . ]]
    }

    task "fastapi" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image = [[ .arad.administrator_service_image | quote ]]
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
