job "application_database" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "application_database" {
    count = 1

    network {
      mode = [[ .arad.network_mode ]]
    }

    [[ template "postgres_consul_service" "application" ]]

    task "postgres" {
      driver = "docker"

      [[ template "kv_access" . ]]

      [[ template "postgres_credentials" "application" ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        [[ template "postgres_config" "user" ]]
      }

      [[ template "resources" .arad.application_database_resources -]]
    }
  }
}
