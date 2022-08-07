job "identity_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "identity_service" {
    network {
      port "http" {
        to = [[ .arad.service_listen_port ]]
      }
    }

    task "fastapi" {
      driver = "docker"

      env {
        DATABASE_URL = "postgresql+asyncpg://arad_user:arad_user@localhost:5432/arad_user"
        CACHE_URL = "redis://localhost:6379/0"
        DEFAULT_ADMIN_EMAIL = "admin@domain.org"
        ACCESS_TOKEN_PUBLIC_KEY_PEM = <<EOK
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEnoH4lyjW4T0uUFbAYRL1G/3dxF1M
kak4CYTwDU8lSubpkIKXFqo7KtsWIycbTKbfLm2IdwNXDOO346u4OhCaBg==
-----END PUBLIC KEY-----
EOK
      ACCESS_TOKEN_PRIVATE_KEY_PEM = <<EOK
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPDn6E30e3lwXXnW1GyYYH942x0OiU/lRhYKYh9IJReaoAoGCCqGSM49
AwEHoUQDQgAEnoH4lyjW4T0uUFbAYRL1G/3dxF1Mkak4CYTwDU8lSubpkIKXFqo7
KtsWIycbTKbfLm2IdwNXDOO346u4OhCaBg==
-----END EC PRIVATE KEY-----
EOK
      }

      config {
        image = [[ .arad.identity_service_image | quote ]]
        ports = ["http"]
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream cache {
{{- range service "token-cache" }}
  server {{ if (eq .Address "127.0.0.1") }}host.docker.internal{{ else }}{{ .Address }}{{ end }}:{{ .Port }};
{{- end }}
}

server {
  listen 6379 so_keepalive=on;
  proxy_pass cache;
}

upstream database {
{{- range service "user-database" }}
  server {{ if (eq .Address "127.0.0.1") }}host.docker.internal{{ else }}{{ .Address }}{{ end }}:{{ .Port }};
{{- end }}
}

server {
  listen 5432 so_keepalive=on;
  proxy_pass database;
}
EOH
        [[ else -]]
        data = <<EOH
upstream cache {
{{- range nomadService "token-cache" }}
  server {{ if (eq .Address "127.0.0.1") }}host.docker.internal{{ else }}{{ .Address }}{{ end }}:{{ .Port }};
{{- end }}
}

server {
  listen 6379 so_keepalive=on;
  proxy_pass cache;
}

upstream database {
{{- range nomadService "user-database" }}
  server {{ if (eq .Address "127.0.0.1") }}host.docker.internal{{ else }}{{ .Address }}{{ end }}:{{ .Port }};
{{- end }}
}

server {
  listen 5432 so_keepalive=on;
  proxy_pass database;
}
EOH
        [[ end -]]
        
        destination = "local/upstreams.conf"
        perms       = 0600
        # command     = "systemctl restart nginx"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
