job "create_application_database" {
  type = "batch"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .batch_jobs.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "create_application_database" {

    network {
      mode = [[ .batch_jobs.network_mode | quote ]]
    }

    service {
      name     = "create-application-database"
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
        entrypoint = ["bash", "-c", "./create-database.sh"]
      }

      env {
        DATABASE_NAME = "arad_application"
      }

      template {
        data = <<EOH
DATABASE_USER="{{ with secret "kv/data/application_database_user" }}{{ .Data.data.value }}{{ end }}"
DATABASE_PASSWORD="{{ with secret "kv/data/application_database_password" }}{{ .Data.data.value }}{{ end }}"
POSTGRES_USER="{{ with secret "kv/data/application_database_postgres_user" }}{{ .Data.data.value }}{{ end }}"
POSTGRES_PASSWORD="{{ with secret "kv/data/application_database_postgres_password" }}{{ .Data.data.value }}{{ end }}"
EOH
        destination = "secrets/.env"
        env = true
      }

      [[ template "resources" .batch_jobs.service_resources ]]
    }
  }
}
