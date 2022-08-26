Kind = "service-intentions"
Name = "user-database"
Sources = [
  {
    Action = "allow"
    Name = "identity-service"
  },
  {
    Action = "allow"
    Name = "create-user-database"
  },
  {
    Action = "allow"
    Name = "migrate-user-database"
  }
]
