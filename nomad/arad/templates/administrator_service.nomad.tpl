job "administrator_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "administrator_service" {
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
        DATABASE_URL = "postgresql+asyncpg://arad_application:arad_application@localhost:5432/arad_application"
      }

      config {
        image       = [[ .arad.administrator_service_image | quote ]]
        ports       = ["http"]
      }

      service {
        name     = "administrator-service"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "http"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream database {
{{- range service "application-database" }}
  server {{ .Address }}:{{ .Port }};
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
  server {{ .Address }}:{{ .Port }};
{{- end }}
}

server {
  listen 5432 so_keepalive=on;
  proxy_pass database;
}
EOH
        [[ end -]]
        
        destination = "local/upstreams.conf"
        # command     = "systemctl restart nginx"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
