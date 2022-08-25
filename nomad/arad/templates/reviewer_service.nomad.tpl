job "reviewer_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reviewer_service" {
    count = [[ .arad.reviewer_service_count ]]

    network {
      mode = [[ .arad.network_mode ]]
    }

    service {
      name = "reviewer-service"
      port     = "80"
      provider = "consul"

      tags = [
        "api.enable=true",
        "api.http.middlewares.reviewer-remove-prefix.stripprefix.prefixes=/api/v1/review",
        "api.http.middlewares.reviewer-remove-prefix.stripprefix.forceSlash=false",
        "api.http.routers.reviewer.tls=true",
        "api.http.routers.reviewer.entrypoints=https",
        "api.http.routers.reviewer.rule=Host(`[[ .arad.api_domain ]]`) && PathPrefix(`/api/v1/review/`)",
        "api.http.routers.reviewer.middlewares=reviewer-remove-prefix@consulcatalog"
      ]

      [[ template "service_database_connect" "application" ]]

      [[ template "service_health_check" . ]]
    }

    task "fastapi" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        image = [[ .arad.reviewer_service_image | quote ]]
      }

      [[ template "application_task_env" . ]]

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
