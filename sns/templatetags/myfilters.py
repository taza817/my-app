from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
import re
from ..models import Tag, QuestionTag

register = template.Library()

@register.filter
def convert_linking_post_tag(text) :
  # tag_words = re.findall(r'(#[^\s]+)', text)
  tag_words = re.findall(r'(#[^\s|<br>]+)', text)
  a_tag = "<a class='{tag_class}' href='{path}'>{tag}</a>"
  for tag_word in tag_words :
    tag_without_sharp = tag_word.replace('#', '')
    tag = Tag.objects.get(name=tag_without_sharp)
    path_to_tag_post_list = reverse('postlist_linking_tag', kwargs={'pk':tag.pk})
    text = text.replace(tag.name, a_tag.format(tag_class='linking_tag',path=path_to_tag_post_list, tag=tag.name))
  return mark_safe(text)

@register.filter
def convert_linking_post_tag_rank(text) :
  a_tag = "<a class='{tag_class}' href='{path}'>{tag}</a>"
  tag = Tag.objects.get(name=text)
  path_to_tag_post_list = reverse('postlist_linking_tag', kwargs={'pk':tag.pk})
  text = text.replace(tag.name, a_tag.format(tag_class='linking_tag',path=path_to_tag_post_list, tag=tag.name))
  return mark_safe(text)
  

@register.filter
def convert_linking_question_tag(text) :
  tag_words = re.findall(r'(#[^\s]+)', text)
  a_tag = "<a class='{tag_class}' href='{path}'>{tag}</a>"
  for tag_word in tag_words :
    tag_without_sharp = tag_word.replace('#', '')
    tag = QuestionTag.objects.get(name=tag_without_sharp)
    path_to_tag_question_list = reverse('questionlist_linking_tag', kwargs={'pk':tag.pk})
    text = text.replace(tag.name, a_tag.format(tag_class='linking_tag',path=path_to_tag_question_list, tag=tag.name))
  return mark_safe(text)

@register.filter
def convert_linking_question_tag_rank(text) :
  a_tag = "<a class='{tag_class}' href='{path}'>{tag}</a>"
  tag = QuestionTag.objects.get(name=text)
  path_to_tag_post_list = reverse('questionlist_linking_tag', kwargs={'pk':tag.pk})
  text = text.replace(tag.name, a_tag.format(tag_class='linking_tag',path=path_to_tag_post_list, tag=tag.name))
  return mark_safe(text)