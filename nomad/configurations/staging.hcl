back_end_allowed_origins = "https://arad-test.org,http://127.0.0.1"
api_domain = "arad-test.org"
front_end_domain = "arad-test.org"

front_end_count = 15
identity_service_count = 10
administrator_service_count = 3
reviewer_service_count = 4
reader_service_count = 12

front_end_image = "jcolburne/arad:front-end-nginx-update-dependencies-latest"
identity_service_image = "jcolburne/arad:identity-update-dependencies-latest"
administrator_service_image = "jcolburne/arad:administrator-update-dependencies-latest"
reviewer_service_image = "jcolburne/arad:reviewer-update-dependencies-latest"
reader_service_image = "jcolburne/arad:reader-update-dependencies-latest"

remote_docker_registry = true
linux_host = true
network_mode = "bridge"
consul_enabled = true
