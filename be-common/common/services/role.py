# from uuid import UUID

# from sqlalchemy import select
# from sqlmodel import Session

from database.models import User


class RoleService:
    # def __init__(self, database: Session):
    #     self.database = database      

    def list_current(self, user: User):
        # doesn't feel like this should live here
        roles = ["READER"]
        if "reviewer" in user.email or "admin" in user.email:
            roles.append("REVIEWER")
        if "admin" in user.email:
            roles.append("ADMINISTRATOR")
          
        return roles

