job "front_end" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "front_end" {
    count = [[ .arad.front_end_count ]]

    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
    }

    service {
      name     = "front-end"
      port     = "80"
      provider = "consul"

      tags = [
        "load-balancer.enable=true",
        "load-balancer.http.routers.front-end.tls=true",
        "load-balancer.http.routers.front-end.entrypoints=https",
        "load-balancer.http.routers.front-end.rule=Host(`[[ .arad.front_end_domain ]]`)"
      ]

      connect {
        sidecar_service {}
      }
    }

    task "nginx" {
      driver = "docker"

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image = [[ .arad.front_end_image | quote ]]
      }

      [[ template "resources" .arad.front_end_resources -]]
    }
  }
}
