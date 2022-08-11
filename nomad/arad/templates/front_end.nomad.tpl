job "front_end" {
  type = "service"

  [[ template "region" . ]]

  datacenters = [ [[ range $idx, $dc := .arad.datacenters ]][[if $idx]],[[end]][[ $dc | quote ]][[ end ]] ]

  group "front_end" {
    network {
      [[ if (.arad.linux_host) ]]
      mode = "bridge"
      [[ end ]]
      port "https" {
        to = 443
        static = 443
      }
    }

    task "react" {
      driver = "docker"

      config {
        [[ if .arad.remote_docker_registry -]]
        force_pull = true
        [[- end ]]
        image = [[ .arad.front_end_image | quote ]]
        ports = ["http"]
      }

      [[ template "resources" .arad.front_end_resources -]]
    }
  }
}
