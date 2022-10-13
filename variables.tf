variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "prod"
}

variable "clientid" {
  sensitive = true
}


variable "clientsecret" {
  sensitive = true
}
