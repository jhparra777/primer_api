import jwt

def crearTokenJWT(data: dict):
    token : str = jwt.encode(data, "misecreto", algorithm="HS256")
    return token

def validateTokenJWT(token: str) -> dict:
    data : dict = jwt.decode(token, "misecreto", algorithms=["HS256"])
    return data
    