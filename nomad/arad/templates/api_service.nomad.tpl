job "api_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api_service" {
    count = 1  // this is temporary, we need a load balancer here

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "https" {
        static = 8443
        to = 443
      }
    }

    service {
      name = "api-service"
      connect {
        sidecar_service {
          proxy {
            upstreams {
              destination_name = "identity-service"
              local_bind_port = 8080
              mesh_gateway {
                mode = "local"
              }
            }
            upstreams {
              destination_name = "administrator-service"
              local_bind_port = 8081
              mesh_gateway {
                mode = "local"
              }
            }
            upstreams {
              destination_name = "reviewer-service"
              local_bind_port = 8082
              mesh_gateway {
                mode = "local"
              }
            }
            upstreams {
              destination_name = "reader-service"
              local_bind_port = 8083
              mesh_gateway {
                mode = "local"
              }
            }
          }
        }
      }
    }

    task "nginx" {
      driver = "docker"

      vault {
        policies = ["kv"]
      }

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image       = [[ .arad.api_service_image | quote ]]
        ports       = ["https"]
      }

      service {
        name     = "api-service"
        port     = "443"
        provider = "consul"
      }

      template {
        [[ template "secret_pem" "api_nginx_private_key" ]]
        destination = "secrets/nginx-private-key.pem"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        [[ template "secret_pem" "api_nginx_certificate" ]]
        destination = "secrets/nginx-certificate.pem"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        data = <<EOH
upstream identity {
  server 127.0.0.1:8080;
{{- $SERVICE_COUNT := len (service "identity-service") -}}
{{- if (gt $SERVICE_COUNT 0) }}
  keepalive {{ multiply $SERVICE_COUNT 2 }};
{{ end -}}
}
EOH
        destination = "local/identity.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        data = <<EOH
upstream administrator {
  server 127.0.0.1:8081;
{{- $SERVICE_COUNT := len (service "administrator-service") -}}
{{- if (gt $SERVICE_COUNT 0) }}
  keepalive {{ multiply $SERVICE_COUNT 2 }};
{{ end -}}
}
EOH
        destination = "local/administrator.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        data = <<EOH
upstream reviewer {
  server 127.0.0.1:8082;
{{- $SERVICE_COUNT := len (service "reviewer-service") -}}
{{- if (gt $SERVICE_COUNT 0) }}
  keepalive {{ multiply $SERVICE_COUNT 2 }};
{{ end -}}
}
EOH
        destination = "local/reviewer.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        data = <<EOH
upstream reader {
  server 127.0.0.1:8083;
{{- $SERVICE_COUNT := len (service "reader-service") -}}
{{- if (gt $SERVICE_COUNT 0) }}
  keepalive {{ multiply $SERVICE_COUNT 2 }};
{{ end -}}
}
EOH
        destination = "local/reader.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
