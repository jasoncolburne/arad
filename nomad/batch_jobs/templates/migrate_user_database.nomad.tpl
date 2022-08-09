job "migrate_user_database" {
  type = "batch"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .batch_jobs.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "migrate_user_database" {
    [[ if (.arad.linux_host) ]]
    network {
      mode = "bridge"
    }
    [[ end ]]

    task "alembic" {
      driver = "docker"

      config {
        image = [[ .batch_jobs.identity_service_image | quote ]]
        entrypoint = ["bash", "-c", "service nginx start && ./migrate.sh"]
      }

      env {
        DATABASE_URL = "postgresql+asyncpg://arad_user:arad_user@localhost:5432/arad_user"
      }

      restart {
        attempts = 0
      }

      template {
        [[ if (.batch_jobs.consul_enabled) -]]
        data = <<EOH
upstream database {
{{- range service "user-database" }}
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
{{- range nomadService "user-database" }}
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
        perms       = 0600
        # command     = "systemctl restart nginx"
      }

      [[ template "resources" .batch_jobs.service_resources -]]
    }
  }
}
