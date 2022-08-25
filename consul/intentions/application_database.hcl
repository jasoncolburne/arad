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
  },
  {
    Action = "allow"
    Name = "create-application-database"
  },
  {
    Action = "allow"
    Name = "migrate-application-database"
  }
]
