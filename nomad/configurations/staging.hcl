back_end_allowed_origins = "https://arad-test.org,http://127.0.0.1"
api_domain = "arad-test.org"
front_end_domain = "arad-test.org"

front_end_count = 15
identity_service_count = 10
administrator_service_count = 3
reviewer_service_count = 4
reader_service_count = 12

front_end_image = "jcolburne/arad:front-end-nginx-database-disconnects-latest"
identity_service_image = "jcolburne/arad:identity-database-disconnects-latest"
administrator_service_image = "jcolburne/arad:administrator-database-disconnects-latest"
reviewer_service_image = "jcolburne/arad:reviewer-database-disconnects-latest"
reader_service_image = "jcolburne/arad:reader-database-disconnects-latest"

remote_docker_registry = true
linux_host = true
network_mode = "bridge"
consul_enabled = true
