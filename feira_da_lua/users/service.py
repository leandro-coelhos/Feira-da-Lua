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

def UpdateUser(user_id: int, username: str = None, complete_name: str = None, password: str = None) -> User:
     """
     Atualiza os detalhes de um usuário existente.

     @param user_id: O ID do usuário a ser atualizado.
     @param username: O novo nome de usuário (opcional).
     @param complete_name: O novo nome completo (opcional).
     @param password: A nova senha (opcional).

     @return O objeto User atualizado.
     """
     user = GetUserById(user_id)
     if username is not None:
          user.username = username
     if complete_name is not None:
          user.complete_name = complete_name
     if password is not None:
          user.password = password
     user.save()

     return user



