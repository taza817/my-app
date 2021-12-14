from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from sns.models import Answer

@receiver(post_save, sender=Answer)
def answer_create_notification(sender, instance, created, **kwargs) :
    """コメントが投稿されたら質問者にメールで通知する"""
    question = instance.question    #コメントされた質問
    account = question.user    #質問を投稿したユーザー

    if created :
        subject = "質問にコメントがつきました"
        massage = "あなたが投稿した質問にコメントがつきました。"
        # context = {
        #   'account' : account,
        #   'question' : question,
        #   'answer' : instance.text,
        # }
        # massage = render_to_string('/mails/answer_create_notification.txt', context)
        from_email = settings.DEFAULT_FROM_EMAIL     #送信者
        recipient_list = [account.user.email]   #宛先
        send_mail(subject, massage, from_email, recipient_list)
