job "load_balancer" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "load_balancer" {
    count = 1  // do not change this, the host will try and bind multiple times on the same port

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
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
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image = "traefik"
        auth_soft_fail = true
        volumes = [
          "local/traefik.toml:/etc/traefik/traefik.toml",
        ]
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

      template {
        data = <<EOF
[[ "[[tls.certificates]]" ]]
certFile = "/secrets/[[ .arad.front_end_domain ]].cert"
keyFile = "/secrets/[[ .arad.front_end_domain ]].key"

[tls.options]
  [tls.options.default]
  minVersion = "VersionTLS12"

  cipherSuites = [
    # 1.3
    "TLS_AES_256_GCM_SHA384",
    "TLS_AES_128_GCM_SHA256",
    "TLS_CHACHA20_POLY1305_SHA256",

    # 1.2
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",

    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",

    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"
  ]

  curvePreferences = ["CurveP521", "CurveP384"]
EOF


        change_mode = "restart"
        destination = "local/dynamic.toml"
      }

      [[ template "resources" .arad.traefik_resources -]]
    }
  }
}
