job "reader_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reader_service" {
    count = [[ .arad.reader_service_count ]]

    network {
      mode = [[ .arad.network_mode ]]
    }

    service {
      name     = "reader-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.reader-remove-prefix.stripprefix.prefixes=/api/v1/read",
        "api.http.middlewares.reader-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.reader.tls=true",
        "api.http.routers.reader.entrypoints=https",
        "api.http.routers.reader.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/read/`)",
        "api.http.routers.reader.middlewares=reader-remove-prefix@consulcatalog"
      ]

      [[ template "service_database_connect" "application" ]]

      [[ template "service_health_check" . ]]
    }

    task "fastapi" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        image = [[ .arad.reader_service_image | quote ]]
      }

      [[ template "application_task_env" . ]]

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
