from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    password_hash: str
    user_role: str
