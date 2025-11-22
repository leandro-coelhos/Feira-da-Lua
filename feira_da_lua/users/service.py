from .models import User

def CreateUser(email: str, username: str, password: str, complete_name: str) -> User:
     """
     Cria um novo usuário

     @param email: O email do usuário.
     @param username: O nome de usuário.
     @param password: A senha do usuário.
     @param complete_name: O nome completo do usuário.

     @return O objeto User criado.
     """
     user = User(email=email, username=username, password=password, complete_name=complete_name)
     user.save()
     return user