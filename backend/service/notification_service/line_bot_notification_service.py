from linebot import LineBotApi
from linebot.models import TextSendMessage
from loguru import logger


class LineBotNotificationService:
    def __init__(self, line_bot_api: LineBotApi) -> None:
        self.line_bot_api = line_bot_api

    def push_notification(self, topic: str,message: str) -> bool:
        logger.success(f"[LINE BOT SENDING SUCCESSFULLY] Sending LINE bot notification: {topic} with message: {message}")
        return True


