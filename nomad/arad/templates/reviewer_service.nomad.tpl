job "reviewer_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "reviewer_service" {
    network {
      port "http" {
        to = [[ .arad.service_listen_port ]]
      }
    }

    task "fastapi" {
      driver = "docker"

      env {
        ALLOWED_ORIGINS = [[ .arad.back_end_allowed_origins | quote ]]
        DATABASE_URL = "postgresql+asyncpg://arad_application:arad_application@localhost:5432/arad_application"
      }

      config {
        image       = [[ .arad.reviewer_service_image | quote ]]
        extra_hosts = ["host.docker.internal:host-gateway"]
        ports       = ["http"]
      }

      service {
        name     = "reviewer-service"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "http"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream database {
{{- range service "application-database" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}

server {
  listen 5432 so_keepalive=on;
  proxy_pass database;
}
EOH
        [[ else -]]
        data = <<EOH
upstream database {
{{- range nomadService "application-database" }}
  server host.docker.internal:{{ .Port }};
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
