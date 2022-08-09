job "api_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api_service" {
    network {
      port "http" {
        to = [[ .arad.service_listen_port ]]
        static = 81
      }
    }

    task "nginx" {
      driver = "docker"

      config {
        image       = [[ .arad.api_service_image | quote ]]
        extra_hosts = ["host.docker.internal:host-gateway"]
        ports       = ["http"]
      }

      service {
        name     = "api-service"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "http"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream administrator {
{{- range service "administrator-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ else -]]
        data = <<EOH
upstream administrator {
{{- range nomadService "administrator-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ end -]]
        
        destination = "local/administrator.conf"
        # command     = "systemctl restart nginx"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream reviewer {
{{- range service "reviewer-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ else -]]
        data = <<EOH
upstream reviewer {
{{- range nomadService "reviewer-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ end -]]
        
        destination = "local/reviewer.conf"
        # command     = "systemctl restart nginx"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream reader {
{{- range service "reader-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ else -]]
        data = <<EOH
upstream reader {
{{- range nomadService "reader-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ end -]]
        
        destination = "local/reader.conf"
        # command     = "systemctl restart nginx"
      }

      template {
        [[ if (.arad.consul_enabled) -]]
        data = <<EOH
upstream identity {
{{- range service "identity-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ else -]]
        data = <<EOH
upstream identity {
{{- range nomadService "identity-service" }}
  server host.docker.internal:{{ .Port }};
{{- end }}
}
EOH
        [[ end -]]
        
        destination = "local/identity.conf"
        # command     = "systemctl restart nginx"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
