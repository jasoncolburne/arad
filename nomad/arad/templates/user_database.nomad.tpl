job "user_database" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this database, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "user_database" {
    count = 1

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "db" {
        to = [[ .arad.user_database_port ]]
      }
    }

    task "postgres" {
      driver = "docker"

      config {
        image          = "postgres:bullseye"
        ports          = ["db"]
        auth_soft_fail = true
        volumes        = ["arad_user_database:/var/lib/postgresql/data"]
        volume_driver  = "local"
      }

      service {
        name     = "user-database"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "db"
      }

      env {
          POSTGRES_USER="postgres"
          POSTGRES_PASSWORD="passphrase"
      }

      [[ template "resources" .arad.user_database_resources -]]
    }
  }
}
