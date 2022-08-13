job "reviewer_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reviewer_service" {
    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name = "reviewer-service"
      port     = "80"
      provider = "consul"
      connect {
        sidecar_service {
          proxy {
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
        image       = [[ .arad.reviewer_service_image | quote ]]
      }

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
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
