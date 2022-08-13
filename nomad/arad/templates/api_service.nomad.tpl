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
        [[ template "upstream_consul" "administrator" ]]
        destination = "local/administrator.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        [[ template "upstream_consul" "reviewer" ]]
        destination = "local/reviewer.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        [[ template "upstream_consul" "reader" ]]
        destination = "local/reader.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      template {
        [[ template "upstream_consul" "identity" ]]
        destination = "local/identity.conf"
        change_mode = "signal"
        change_signal = "SIGHUP"
      }

      [[ template "resources" .arad.service_resources -]]
    }
  }
}
