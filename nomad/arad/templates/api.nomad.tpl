job "api" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api" {
    count = 1  // do not change this, the host will try and bind multiple times on the same port

    network {
      mode = [[ .arad.network_mode | quote ]]
      port "https" {
        static = [[ .arad.api_port ]]
      }
    }

    service {
      name     = "api"
      port     = [[ .arad.api_port | quote ]]
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
      }

      template {
        [[ template "secret_pem" "api_private_key" ]]
        destination = "secrets/[[ .arad.api_domain ]].key"
        change_mode = "restart"
      }

      template {
        [[ template "secret_pem" "api_certificate" ]]
        destination = "secrets/[[ .arad.api_domain ]].cert"
        change_mode = "restart"
      }

      template {
        data = <<EOF
defaultEntrypoints = ["https"]

[entryPoints]
  [entryPoints.https]
  address = ":[[ .arad.api_port ]]"

[providers]
  [providers.file]
      filename = "/local/dynamic.toml"

  [providers.consulCatalog]
  prefix           = "api"
  serviceName      = "api"
  connectAware     = true
  connectByDefault = true
  exposedByDefault = false

    [providers.consulCatalog.endpoint]
    address = "unix:///alloc/tmp/consul_http.sock"
    scheme  = "http"
    token   = "{{- with secret "kv/data/api_consul_token" -}}{{ .Data.data.value  }}{{- end -}}"
EOF

        change_mode = "restart"
        destination = "local/traefik.toml"
      }

      [[ template "traefik_dynamic_config" .arad.api_domain ]]

      [[ template "resources" .arad.traefik_resources ]]
    }
  }
}
