from typing import List
from pydantic import BaseSettings,ValidationError

class EnvVars(BaseSettings):
    #mongodb
    mongodb_localhost:str

    #mqtt configuration
    mqtt_broker:str
    mqtt_port:int

    #sparrow sms
    time_interval_to_send_sms:int
    sparrow_token:str
    sparrow_from:str
    sparrow_to:str

    
    class Config:
        env_file=".env"
try:
    env=EnvVars()  
    print(env.__dict__)
except ValidationError as e:
    print(e.json())