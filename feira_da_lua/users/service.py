from .models import User, Marketer, Avaliation

## User Services

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
     try:
          user = User.objects.get(id=user_id)
     except User.DoesNotExist:
          return None
     return user

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

def DeleteUser(user_id: int) -> None:
     """
     Deleta um usuário pelo seu ID.

     @param user_id: O ID do usuário a ser deletado.
     """
     user = GetUserById(user_id)
     user.delete()

     return None


## Marketer Services

def CreateMarketer(email: str, username: str, password: str, complete_name: str, cellphone: str) -> Marketer:
     """
     Cria um novo marketer.

     @param email: O email do marketer.
     @param username: O nome de usuário do marketer.
     @param password: A senha do marketer.
     @param complete_name: O nome completo do marketer.
     @param cellphone: O celular do marketer.

     @return O objeto Marketer criado.
     """
     user = CreateUser(email=email, username=username, password=password, complete_name=complete_name)
     marketer = Marketer(user=user, cellphone=cellphone)
     marketer.save()
     return marketer

def GetMarketerById(marketer_id: int) -> Marketer:
     """
     Recupera um marketer pelo seu ID.

     @param marketer_id: O ID do marketer.

     @return O objeto Marketer correspondente ao ID fornecido.
     """
     try:
          marketer = Marketer.objects.get(user__id=marketer_id)
     except Marketer.DoesNotExist:
          return None
     return marketer

def GetMarketerByEmail(email: str) -> Marketer:
     """
     Recupera um marketer pelo seu email.

     @param email: O email do marketer.

     @return O objeto Marketer correspondente ao email fornecido.
     """
     user = GetUserByEmail(email)
     try:
          marketer = Marketer.objects.get(user=user)
     except Marketer.DoesNotExist:
          return None
     return marketer

def UpdateMarketer(marketer_id: int, username: str = None, complete_name: str = None, password: str = None, cellphone: str = None) -> Marketer:
     """
     Atualiza os detalhes de um marketer existente.

     @param marketer_id: O ID do marketer a ser atualizado.
     @param username: O novo nome de usuário (opcional).
     @param complete_name: O novo nome completo (opcional).
     @param password: A nova senha (opcional).
     @param cellphone: O novo celular (opcional).

     @return O objeto Marketer atualizado.
     """
     marketer = GetMarketerById(marketer_id)
     user = marketer.user
     if username is not None:
          user.username = username
     if complete_name is not None:
          user.complete_name = complete_name
     if password is not None:
          user.password = password
     user.save()
     if cellphone is not None:
          marketer.cellphone = cellphone
     marketer.save()

     return marketer

def DeleteMarketer(marketer_id: int) -> None:
     """
     Deleta um marketer pelo seu ID.

     @param marketer_id: O ID do marketer a ser deletado.
     """
     marketer = GetMarketerById(marketer_id)
     user = marketer.user
     marketer.delete()
     user.delete()

     return None

# Avaliation Services

def CreateAvaliation(user: User, marketplace, grade: int, comment: str) -> Avaliation:
     """
     Cria uma nova avaliação.

     @param user: O usuário que faz a avaliação.
     @param marketplace: O marketplace sendo avaliado.
     @param grade: A nota da avaliação.
     @param comment: O comentário da avaliação.

     @return O objeto Avaliation criado.
     """
     avaliation = Avaliation(user=user, marketplace=marketplace, grade=grade, comment=comment)
     avaliation.save()
     return avaliation