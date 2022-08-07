job "application_database" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this database, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "application_database" {
    count = 1

    network {
      port "db" {
        to = [[ .arad.application_database_port ]]
      }
    }

    task "postgres" {
      driver = "docker"

      config {
        image          = "postgres:bullseye"
        ports          = ["db"]
        auth_soft_fail = true
        volumes        = ["arad_application_database:/var/lib/postgresql/data"]
        volume_driver  = "local"
      }

      service {
        name     = "application-database"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "db"
      }

      env {
          POSTGRES_USER="postgres"
          POSTGRES_PASSWORD="passphrase"
      }

      [[ template "resources" .arad.application_database_resources -]]
    }
  }
}
