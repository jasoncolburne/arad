back_end_allowed_origins = "https://arad-test.org,http://127.0.0.1"
api_domain = "arad-test.org"
front_end_domain = "arad-test.org"

front_end_count = 15
identity_service_count = 10
administrator_service_count = 3
reviewer_service_count = 4
reader_service_count = 12

front_end_image = "jcolburne/arad:front-end-nginx-working-repl-latest"
identity_service_image = "jcolburne/arad:identity-working-repl-latest"
administrator_service_image = "jcolburne/arad:administrator-working-repl-latest"
reviewer_service_image = "jcolburne/arad:reviewer-working-repl-latest"
reader_service_image = "jcolburne/arad:reader-working-repl-latest"

service_resources = {
    cpu    = 500,
    memory = 420
}

remote_docker_registry = true
linux_host = true
network_mode = "bridge"
consul_enabled = true
