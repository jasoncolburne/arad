job "identity_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "identity_service" {
    count = 5

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name     = "identity-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.identity-remove-prefix.replacepathregex.regex=^/api/v1/identify/(.*)",
        "api.http.middlewares.identity-remove-prefix.replacepathregex.replacement=/$1",
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
        image       = [[ .arad.identity_service_image | quote ]]
      }

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
        CACHE_URL = "redis://localhost:6379/0"
        DEFAULT_ADMIN_EMAIL = "admin@domain.org"
      }

      template {
        data = <<EOH
DATABASE_URL="{{ with secret "kv/data/user_database_url" }}{{ .Data.data.value }}{{ end }}"
ACCESS_TOKEN_PRIVATE_KEY_PEM={{ with secret "kv/data/access_token_private_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}
ACCESS_TOKEN_PUBLIC_KEY_PEM={{ with secret "kv/data/access_token_public_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}
EOH
        destination = "secrets/.env"
        env = true
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
