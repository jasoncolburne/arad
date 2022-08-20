key_prefix "front-end-load-balancer" {
  policy = "write"
}

service "front-end-load-balancer" {
  policy = "write"
}

agent_prefix "" {
  policy = "read"
}

node_prefix "" {
  policy = "read"
}

service_prefix "" {
  policy = "read"
}
