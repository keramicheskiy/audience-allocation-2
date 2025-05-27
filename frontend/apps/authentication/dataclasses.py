from dataclasses import dataclass


@dataclass
class User:
    id: str
    first_name: str
    patronymic: str
    last_name: str
    email: str
    role: str
    is_verified: bool


@dataclass
class RegistrationUser:
    first_name: str
    patronymic: str
    last_name: str
    email: str
    role: str
    password: str


@dataclass
class LoginUser:
    email: str
    password: str

