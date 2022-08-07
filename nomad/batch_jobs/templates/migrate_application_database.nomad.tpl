job "migrate_application_database" {
  type = "batch"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .batch_jobs.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "migrate_application_database" {
    task "alembic" {
      driver = "docker"

      config {
        image = [[ .batch_jobs.administrator_service_image | quote ]]
        entrypoint = ["bash", "-c", "service nginx start && ./migrate.sh"]
      }

      restart {
        attempts = 0
      }

      template {
        [[ if (.batch_jobs.consul_enabled) -]]
        data = <<EOH
upstream database {
{{- range service "application-database" }}
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
upstream database {
{{- range nomadService "application-database" }}
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

      [[ template "resources" .batch_jobs.service_resources -]]
    }
  }
}
