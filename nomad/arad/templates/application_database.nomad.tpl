job "application_database" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this database, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "application_database" {
    count = 1

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "db" {
        to = [[ .arad.application_database_port ]]
      }
    }

    task "postgres" {
      driver = "docker"

      env {
          POSTGRES_USER="postgres"
          POSTGRES_PASSWORD="passphrase"
      }

      config {
        image          = "postgres:bullseye"
        ports          = ["db"]
        auth_soft_fail = true
        volumes        = ["arad_application_database:/var/lib/postgresql/data"]
        volume_driver  = "local"
      }

      service {
        name     = "application-database"
        port     = "db"
        provider = "consul"
      }

      [[ template "resources" .arad.application_database_resources -]]
    }
  }
}
