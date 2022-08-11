job "identity_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "identity_service" {
    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "http" {
        to = [[ .arad.service_listen_port ]]
      }
    }

    task "fastapi" {
      driver = "docker"

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
        CACHE_URL = "redis://localhost:6379/0"
        DEFAULT_ADMIN_EMAIL = "admin@domain.org"
      }

      template {
        data = <<EOH
DATABASE_URL="{{ with secret "secret/user_database_url" }}{{ .Data.data.value }}{{ end }}"
ACCESS_TOKEN_PRIVATE_KEY_PEM="{{ with secret "secret/access_token_private_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}"
ACCESS_TOKEN_PUBLIC_KEY_PEM="{{ with secret "secret/access_token_public_key_pem" }}{{ .Data.data.value | toJSON }}{{ end }}"
EOH
        destination = "secrets/.env"
        env = true
      }

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image       = [[ .arad.identity_service_image | quote ]]
        ports       = ["http"]
      }

      service {
        name     = "identity-service"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "http"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream cache {
{{- range service "token-cache" }}
  server 10.1.0.1:{{ .Port }};
{{- end }}
}

server {
  listen 6379 so_keepalive=on;
  proxy_pass cache;
}

upstream database {
{{- range service "user-database" }}
  server 10.1.0.1:{{ .Port }};
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
  server 10.1.0.1:{{ .Port }};
{{- end }}
}

server {
  listen 6379 so_keepalive=on;
  proxy_pass cache;
}

upstream database {
{{- range nomadService "user-database" }}
  server 10.1.0.1:{{ .Port }};
{{- end }}
}

server {
  listen 5432 so_keepalive=on;
  proxy_pass database;
}
EOH
        [[ end -]]
        
        destination = "local/upstreams.conf"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
