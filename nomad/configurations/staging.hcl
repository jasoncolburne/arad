back_end_allowed_origins = "https://arad-test.org"
api_domain = "arad-test.org"
front_end_domain = "arad-test.org"

front_end_count = 15
identity_service_count = 10
administrator_service_count = 3
reviewer_service_count = 4
reader_service_count = 12

front_end_image = "jcolburne/arad:front-end-nginx-main-latest"
identity_service_image = "jcolburne/arad:identity-fix-db-dropping-latest"
administrator_service_image = "jcolburne/arad:administrator-main-latest"
reviewer_service_image = "jcolburne/arad:reviewer-main-latest"
reader_service_image = "jcolburne/arad:reader-main-latest"

remote_docker_registry = true
linux_host = true
consul_enabled = true
