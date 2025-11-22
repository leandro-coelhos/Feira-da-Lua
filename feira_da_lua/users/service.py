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

def GetUserById(user_id: int) -> User:
     """
     Recupera um usuário pelo seu ID.

     @param user_id: O ID do usuário.

     @return O objeto User correspondente ao ID fornecido.
     """
     return User.objects.get(id=user_id)

def GetUserByEmail(email: str) -> User:
     """
     Recupera um usuário pelo seu email.

     @param email: O email do usuário.

     @return O objeto User correspondente ao email fornecido.
     """
     return User.objects.get(email=email)

