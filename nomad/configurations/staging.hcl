back_end_allowed_origins = "https://arad-test.org"
api_domain = "arad-test.org"
front_end_domain = "arad-test.org"

front_end_count = 5
identity_service_count = 5

front_end_image = "jcolburne/arad:front-end-nginx-traefik-api-latest"
identity_service_image = "jcolburne/arad:identity-main-latest"
administrator_service_image = "jcolburne/arad:administrator-main-latest"
reviewer_service_image = "jcolburne/arad:reviewer-main-latest"
reader_service_image = "jcolburne/arad:reader-main-latest"

remote_docker_registry = true
linux_host = true
consul_enabled = true
