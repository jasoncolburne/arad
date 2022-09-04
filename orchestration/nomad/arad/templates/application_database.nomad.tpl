job "application_database" {
  type = "service"

  [[ template "region" . ]]

  datacenters = ["dc1"]

  group "application_database" {
    count = 1

    network {
      mode = [[ .arad.network_mode | quote ]]
    }

    [[ template "postgres_consul_service" "application" ]]

    task "postgres" {
      driver = "docker"

      [[ template "kv_access" . ]]

      [[ template "postgres_credentials" "application" ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        [[ template "postgres_task_config" "application" ]]
      }

      [[ template "postgres_config" . ]]

      [[ template "resources" .arad.application_database_resources ]]
    }
  }
}
