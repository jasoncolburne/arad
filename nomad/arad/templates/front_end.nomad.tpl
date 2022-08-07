job "front_end" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "front_end" {
    network {
      port "http" {
        to = [[ .arad.service_listen_port ]]
        static = 80
      }
    }

    task "react" {
      driver = "docker"

      config {
        image = [[ .arad.front_end_image | quote ]]
        ports = ["http"]
      }

      [[ template "resources" .arad.front_end_resources -]]
    }
  }
}
