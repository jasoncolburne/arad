variable "consul_enabled" {
  description = "If Consul is configured for this deployment."
  type        = bool
  default     = false
}

variable "datacenters" {
  description = "A list of datacenters in the region which are eligible for task placement. The first datacenter in the list will be used for uniquely deployed infrastructure."
  type        = list(string)
  default     = ["dc1","dc2"]
}

variable "region" {
  description = "The region where the job should be placed."
  type        = string
  default     = "global"
}

variable "token_cache_port" {
  description = "The port to listen on."
  type = number
  default = 6379
}

variable "token_cache_resources" {
  description = "The resources to assign to the cache."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 500,
    memory = 256
  }
}

variable "user_database_port" {
  description = "The port to listen on."
  type = number
  default = 5432
}

variable "user_database_resources" {
  description = "The resources to assign to the user database."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 1000,
    memory = 768
  }
}

variable "application_database_port" {
  description = "The port to listen on."
  type = number
  default = 5432
}

variable "application_database_resources" {
  description = "The resources to assign to the user database."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 1000,
    memory = 768
  }
}

variable "service_listen_port" {
  description = "The port services will listen on."
  type = number
  default = 80
}

variable "service_resources" {
  description = "The resources to assign to the user database."
  type = object({
    cpu    = number
    memory = number
  })
  default = {
    cpu    = 750,
    memory = 512
  }
}

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

variable "administrator_service_image" {
  description = "The image to use for the administrator service."
  type = string
  default = "arad_administrator:local"
}
