job "api_service" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "api_service" {
    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "http" {
        to = [[ .arad.service_listen_port ]]
        static = 8080
      }
    }

    task "nginx" {
      driver = "docker"

      config {
        image       = [[ .arad.api_service_image | quote ]]
        ports       = ["http"]
      }

      service {
        name     = "api-service"
        provider = [[ if (.arad.consul_enabled) -]]"consul"[[- else -]]"nomad"[[- end ]]
        port     = "http"
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
