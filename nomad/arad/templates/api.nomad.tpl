job "api" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api" {
    count = 1  // do not change this, the host will try and bind multiple times on the same port

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "https" {
        static = 8443
      }
    }

    service {
      name     = "api"
      provider = "consul"
      port     = "https"

      connect {
        native = true
      }
    }

    task "traefik" {
      driver = "docker"

      vault {
        policies = ["kv"]
      }

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
        [[ template "secret_pem" "api_nginx_private_key" ]]
        destination = "secrets/private-key.pem"
        change_mode = "restart"
      }

      template {
        [[ template "secret_pem" "api_nginx_certificate" ]]
        destination = "secrets/certificate.pem"
        change_mode = "restart"
      }

      template {
        data = <<EOF
[entryPoints]
  [entryPoints.websecure]
    address = ":8443"

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

[[ "[[tls.certificates]]" ]]
  certFile = "/secrets/certificate.pem"
  keyFile = "/secrets/private-key.pem"

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
        destination = "local/traefik.toml"
      }

      [[ template "resources" .arad.api_resources -]]
    }
  }
}
