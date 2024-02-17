

import smtplib
import ssl
import time
from email.message import EmailMessage
from threading import Thread

from loguru import logger

from repository.email_receiver_repository import EmailReceiverRepository
from repository.gmail_notification_config_repository import \
    GmailNotificationConfigRepository
from service.notification_service.base_notification_service import \
    BaseNotificationService


class GmailNotificationService(BaseNotificationService):
    def __init__(self, publication_interval: int, email_receiver_repository: EmailReceiverRepository, gmail_config_repo: GmailNotificationConfigRepository) -> None:
        
        self.email_receiver_repository = email_receiver_repository
        self.gmail_config_repo = gmail_config_repo
        self.publication_interval = publication_interval
        
        self.topic_rate_limit_map: dict[str, float] = {}
        
        
        self.email_queue: list[EmailMessage] = []
        
        
        self._handle_email_messages()
    
    
    def get_last_publication_time(self, topic: str) -> float:
        return self.topic_rate_limit_map.get(topic, 0)

    def get_next_publishable_epoch_second_topic(self, topic: str) -> float:
        return (self.get_last_publication_time(topic) + self.publication_interval)

    def _can_publish(self, topic: str, current_epoch_second: float) -> bool:
        return current_epoch_second > self.get_next_publishable_epoch_second_topic(topic)
    
    
    def _create_email_message(self, _from: str, _to: str, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = _from
        message["To"] =_to
        message["Subject"] = subject
        message.set_content(content)
        return message

    def push_notification(self, topic: str,message: str) -> bool:
        current_epoch_second = time.time()
        if not self._can_publish(topic,current_epoch_second):
            logger.warning(f"[GMAIL RATE LIMIT] Current time for topic {topic} is unavailable, please wait for {int(self.get_next_publishable_epoch_second_topic(topic) - current_epoch_second)} seconds")
            return False

        for receiver in self.email_receiver_repository.find_all():
            email_message = self._create_email_message(self.gmail_config_repo.config.email_sender, receiver.email, topic, message)
            self.email_queue.append(email_message)

        
        self.topic_rate_limit_map[topic] = current_epoch_second

        return True
    
    def _send_gmail(self, email_message: EmailMessage) -> bool:
        
        try:
            with (smtplib.SMTP("smtp.gmail.com", 587) as smtp):
                smtp.starttls()
                sender = self.gmail_config_repo.config.email_sender
                smtp.login(sender, self.gmail_config_repo.config.password)
                smtp.sendmail(sender, email_message["To"], email_message.as_string())
                logger.success(f"[GMAIL SENDING SUCCESSFULLY] Sending email: {email_message}")
        except Exception as error:
            logger.error(error)
            return False
        
        return True
    
    def _handle_email_messages(self) -> None:
        def wrapper() -> None:
            while (True):
                time.sleep(1)
                if len(self.email_queue) == 0:
                    continue
                
                email_message = self.email_queue.pop(0)
                is_sent = self._send_gmail(email_message)
                if not is_sent:
                    self.email_queue.append(email_message)
                    
        
        Thread(target = wrapper).start()
            
