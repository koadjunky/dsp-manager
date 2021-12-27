from dataclasses import dataclass


@dataclass
class Config:
    veins_utilization: int = 0


config = Config()
#TODO: put config in database
