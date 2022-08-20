key_prefix "load-balancer" {
  policy = "write"
}

service "load-balancer" {
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
