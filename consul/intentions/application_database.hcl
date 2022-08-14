Kind = "service-intentions"
Name = "application-database"
Sources = [
  {
    Action = "allow"
    Name = "administrator-service"
  },
  {
    Action = "allow"
    Name = "reviewer-service"
  },
  {
    Action = "allow"
    Name = "reader-service"
  }
]
