////////////////////////////////////////////////////////////////////////////////////////////////////
// General
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "region" {
  description = "The region where the job should be placed."
  type        = string
  default     = "global"
}

variable "datacenters" {
  description = "A list of datacenters in the region which are eligible for task placement. The first datacenter in the list will be used for uniquely deployed infrastructure."
  type        = list(string)
  default     = ["dc1"]
}

variable "remote_docker_registry" {
  description = "Whether to use a remote registry."
  type = bool
  default = false
}

variable "linux_host" {
  description = "Whether the host OS is Linux."
  type = bool
  default = false
}

variable "network_mode" {
  description = "The network mode to use."
  type = string
  default = "host"
}

variable "consul_enabled" {
  description = "If Consul is configured for this deployment."
  type        = bool
  default     = false
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Ports
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "token_cache_port" {
  description = "The port to listen on."
  type = number
  default = 6379
}

variable "user_database_port" {
  description = "The port to listen on."
  type = number
  default = 5432
}

variable "application_database_port" {
  description = "The port to listen on."
  type = number
  default = 5432
}

variable "front_end_port" {
  description = "The public port to listen on."
  type = number
  default = 443
}

variable "api_port" {
  description = "The public port to listen on."
  type = number
  default = 8443
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Resources
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "token_cache_resources" {
  description = "The resources to assign to the cache."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 250,
    memory = 128
  }
}

variable "user_database_resources" {
  description = "The resources to assign to the user database."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 500,
    memory = 256
  }
}

variable "application_database_resources" {
  description = "The resources to assign to the user database."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 500,
    memory = 256
  }
}

variable "service_resources" {
  description = "The resources to assign to a backend service."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 500,
    memory = 256
  }
}

variable "front_end_resources" {
  description = "The resources to assign to the front-end."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 100,
    memory = 64
  }
}

variable "traefik_resources" {
  description = "The resources to assign to the api load balancer."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 100,
    memory = 128
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Domains
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "api_domain" {
  description = "The domain for the api gateway."
  type = string
  default = "localhost"
}

variable "front_end_domain" {
  description = "The domain for the front end."
  type = string
  default = "localhost"
}

variable "back_end_allowed_origins" {
  description = "A string, comma separated list of origins to allow access to the backend. eg, https://arad.org"
  type = string
  default = "http://arad-local.org"
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Images
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "identity_service_image" {
  description = "The image to use for the identity service."
  type = string
  default = "arad_identity:local"
}

variable "reader_service_image" {
  description = "The image to use for the reader service."
  type = string
  default = "arad_reader:local"
}

variable "reviewer_service_image" {
  description = "The image to use for the reviewer service."
  type = string
  default = "arad_reviewer:local"
}

variable "administrator_service_image" {
  description = "The image to use for the administrator service."
  type = string
  default = "arad_administrator:local"
}

variable "front_end_image" {
  description = "The image to use for the front-end."
  type = string
  default = "arad_front-end-nginx:local"
}

////////////////////////////////////////////////////////////////////////////////////////////////////
// Scaling
////////////////////////////////////////////////////////////////////////////////////////////////////

variable "identity_service_count" {
  description = "Desired count."
  type = number
  default = 2
}

variable "administrator_service_count" {
  description = "Desired count."
  type = number
  default = 2
}

variable "reviewer_service_count" {
  description = "Desired count."
  type = number
  default = 2
}

variable "reader_service_count" {
  description = "Desired count."
  type = number
  default = 2
}

variable "front_end_count" {
  description = "Desired count."
  type = number
  default = 2
}
