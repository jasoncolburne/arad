job "migrate_application_database" {
  type = "batch"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .batch_jobs.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "migrate_application_database" {

    network {
      mode = [[ .batch_jobs.network_mode | quote ]]
    }

    service {
      name     = "migrate-application-database"
      provider = "consul"

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
    }

    task "alembic" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        force_pull = [[ .batch_jobs.remote_docker_registry ]]
        image = [[ .batch_jobs.administrator_service_image | quote ]]
        entrypoint = ["./migrate.sh"]
      }

      template {
        data = <<EOH
DATABASE_URL="postgresql+asyncpg://{{ with secret "kv/data/application_database_user" }}{{ .Data.data.value }}{{ end }}:{{ with secret "kv/data/application_database_password" }}{{ .Data.data.value }}{{ end }}@127.0.0.1:5432/batch_jobs_user"
EOH
        destination = "secrets/.env"
        env = true
      }

      [[ template "resources" .batch_jobs.service_resources ]]
    }
  }
}
