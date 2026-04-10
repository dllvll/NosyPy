from dataclasses import dataclass

@dataclass
class Config:
    timeout: int
    delay: int