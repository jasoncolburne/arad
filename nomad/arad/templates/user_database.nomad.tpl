job "user_database" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "user_database" {
    count = 1

    network {
      mode = [[ .arad.network_mode | quote ]]
    }

    [[ template "postgres_consul_service" "user" ]]

    task "postgres" {
      driver = "docker"

      [[ template "kv_access" . ]]

      [[ template "postgres_credentials" "user" ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        [[ template "postgres_task_config" "user" ]]
      }

      [[ template "postgres_config" . ]]

      [[ template "resources" .arad.user_database_resources ]]
    }
  }
}
