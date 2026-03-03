from pydantic import BaseModel


class BotConfig(BaseModel):
    discord_token: str
    grpc_endpoint: str = "localhost:5001"
    rabbitmq_url: str = "amqp://guest:guest@localhost/"
    command_prefix: str = "!"
