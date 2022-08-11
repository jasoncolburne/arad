job "api_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api_service" {
    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "https" {
        to = 443
        static = 8080
      }
    }

    task "nginx" {
      driver = "docker"

      config {
        [[ if .arad.remote_docker_registry -]]
        auth {
          username = [[ with secret "secret/dockerhub_username" -]]
[[ .Data.data.value ]]
{{- end -}}

        }

        force_pull = true
        [[- end ]]
        image       = [[ .arad.api_service_image | quote ]]
        ports       = ["https"]
      }

      // service {
      //   name     = "api-service"
      //   provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
      //   port     = "https"
      // }

      template {
        [[ template "secret_pem" "api_nginx_private_key" ]]

        destination = "secrets/nginx-private-key.pem"
      }

      template {
        [[ template "secret_pem" "api_nginx_certificate" ]]

        destination = "secrets/nginx-certificate.pem"
      }

      template {
        [[ if .arad.consul_enabled ]]
          [[ template "upstream_consul" "administrator" ]]
        [[ else ]]
          [[ template "upstream_nomad" "administrator" ]]
        [[ end ]]
        
        destination = "local/administrator.conf"
      }

      template {
        [[ if .arad.consul_enabled ]]
          [[ template "upstream_consul" "reviewer" ]]
        [[ else ]]
          [[ template "upstream_nomad" "reviewer" ]]
        [[ end ]]

        destination = "local/reviewer.conf"
      }

      template {
        [[ if .arad.consul_enabled ]]
          [[ template "upstream_consul" "reader" ]]
        [[ else ]]
          [[ template "upstream_nomad" "reader" ]]
        [[ end ]]
        
        destination = "local/reader.conf"
      }

      template {
        [[ if .arad.consul_enabled ]]
          [[ template "upstream_consul" "identity" ]]
        [[ else ]]
          [[ template "upstream_nomad" "identity" ]]
        [[ end ]]
        
        destination = "local/identity.conf"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
