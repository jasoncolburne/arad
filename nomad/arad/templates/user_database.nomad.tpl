job "user_database" {
  type = "service"

  [[ template "region" . ]]

  // we only want a single instance of this database, so we won't iterate
  datacenters = [ [[ (index .arad.datacenters 0) | quote ]] ]

  group "user_database" {
    count = 1

    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    service {
      name     = "user-database"
      port     = "5432"
      provider = "consul"
      connect {
        sidecar_service {}
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
        auth_soft_fail = true
        volumes        = ["arad_user_database:/var/lib/postgresql/data"]
        volume_driver  = "local"
      }

      [[ template "resources" .arad.user_database_resources -]]
    }
  }
}
