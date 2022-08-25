job "administrator_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "administrator_service" {
    count = [[ .arad.administrator_service_count ]]

    network {
      mode = [[ .arad.network_mode | quote ]]
    }

    service {
      name = "administrator-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.administrator-remove-prefix.stripprefix.prefixes=/api/v1/administrate",
        "api.http.middlewares.administrator-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.administrator.tls=true",
        "api.http.routers.administrator.entrypoints=https",
        "api.http.routers.administrator.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/administrate/`)",
        "api.http.routers.administrator.middlewares=administrator-remove-prefix@consulcatalog"
      ]

      [[ template "service_database_connect" "application" ]]

      [[ template "service_health_check" . ]]
    }

    task "fastapi" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        image = [[ .arad.administrator_service_image | quote ]]
      }

      [[ template "application_task_env" . ]]

      [[ template "resources" .arad.service_resources ]]
    }
  }
}
