import asyncio
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from config import notification_settings  # type: ignore

fastmail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump(),
    )
)


async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["yavut@mailto.plus"],
            subject="Your Email Delivered With FastShip",
            body="Things are about to get interesting...",
            subtype=MessageType.plain,
        )
    )
    print("Email sent!")


asyncio.run(send_message())
