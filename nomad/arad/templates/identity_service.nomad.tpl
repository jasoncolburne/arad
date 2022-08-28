job "identity_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "identity_service" {
    count = [[ .arad.identity_service_count ]]

    network {
      mode = [[ .arad.network_mode | quote ]]
    }

    service {
      name     = "identity-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.identity-remove-prefix.stripprefix.prefixes=/api/v1/identify",
        "api.http.middlewares.identity-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.identity.tls=true",
        "api.http.routers.identity.entrypoints=https",
        "api.http.routers.identity.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/identify/`)",
        "api.http.routers.identity.middlewares=identity-remove-prefix@consulcatalog"
      ]

      connect {
        sidecar_service {
          proxy {
            config {
              protocol = "tcp"
              mode = "transparent"
            }

            upstreams {
              destination_name = "user-database"
              local_bind_port  = 5432
              mesh_gateway {
                mode = "local"
              }
            }

            upstreams {
              destination_name = "token-cache"
              local_bind_port  = 6379
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
        force_pull = [[ .arad.remote_docker_registry ]]
        image = [[ .arad.identity_service_image | quote ]]
        [[ template "logging_config" . ]]
      }

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
        CACHE_URL = "redis://localhost:6379/0"
        DEFAULT_ADMIN_EMAIL = "admin@domain.org"
        LISTEN_IP = "127.0.0.1"
      }

      template {
        data = <<EOH
DATABASE_URL="postgresql+asyncpg://{{ with secret "kv/data/user_database_user" }}{{ .Data.data.value }}{{ end }}:{{ with secret "kv/data/user_database_password" }}{{ .Data.data.value }}{{ end }}@127.0.0.1:5432/arad_user"
ACCESS_TOKEN_PRIVATE_KEY_PEM={{ with secret "kv/data/access_token_private_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}
ACCESS_TOKEN_PUBLIC_KEY_PEM={{ with secret "kv/data/access_token_public_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}
EOH
        destination = "secrets/.env"
        env = true
      }

      [[ template "resources" .arad.service_resources ]]
    }
  }
}
