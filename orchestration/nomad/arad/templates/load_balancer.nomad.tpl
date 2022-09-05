job "load_balancer" {
  type = "service"

  [[ template "region" . ]]

  datacenters = ["dc1"]

  group "load_balancer" {
    count = 1  // do not change this, the host will try and bind multiple times on the same port

    network {
      mode = [[ .arad.network_mode | quote ]]
      port "https" {
        static = [[ .arad.front_end_port ]]
      }
    }

    service {
      name     = "load-balancer"
      port     = [[ .arad.front_end_port | quote ]]
      provider = "consul"

      connect {
        native = true
      }
    }

    task "traefik" {
      driver = "docker"

      [[ template "kv_access" . ]]

      config {
        force_pull = [[ .arad.remote_docker_registry ]]
        [[ template "traefik_task_config" . ]]
        [[ template "logging_config" "arad.load_balancer" ]]
      }

      template {
        [[ template "secret_pem" "front_end_private_key" ]]
        destination = "secrets/[[ .arad.front_end_domain ]].key"
        change_mode = "restart"
      }

      template {
        [[ template "secret_pem" "front_end_certificate" ]]
        destination = "secrets/[[ .arad.front_end_domain ]].cert"
        change_mode = "restart"
      }

      template {
        data = <<EOF
defaultEntrypoints = ["https"]

[entryPoints]
  [entryPoints.https]
  address = ":[[ .arad.front_end_port ]]"

[providers]
  [providers.file]
      filename = "/local/dynamic.toml"

  [providers.consulCatalog]
  prefix           = "load-balancer"
  serviceName      = "load-balancer"
  connectAware     = true
  connectByDefault = true
  exposedByDefault = false

    [providers.consulCatalog.endpoint]
    address = "unix:///alloc/tmp/consul_http.sock"
    scheme  = "http"
    token   = "{{- with secret "kv/data/load_balancer_consul_token" -}}{{ .Data.data.value  }}{{- end -}}"
EOF

        change_mode = "restart"
        destination = "local/traefik.toml"
      }

      [[ template "traefik_dynamic_config" .arad.front_end_domain ]]

      [[ template "resources" .arad.traefik_resources ]]
    }
  }
}
