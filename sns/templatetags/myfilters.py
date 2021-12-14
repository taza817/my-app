from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def convert_linking_post_tag(text) :
  path_to_tag_post_list = reverse('postlist_linking_tag')
  # path_to_tag_post_list = "/post/search/?query=%23{}".format(text)
  a_tag = "<a class='{tag_class}' href='{path}?tag_word={tag}'>{tag}</a>"
  text_with_linking_tag = re.sub(r'(#[^\s]+)', a_tag.format(tag_class='linking_tag', path=path_to_tag_post_list, tag='\\1'), text)
  return mark_safe(text_with_linking_tag)
  
@register.filter
def convert_linking_question_tag(text) :
  path_to_tag_post_list = reverse('questionlist_linking_tag')
  # path_to_tag_post_list = "/post/search/?query={}".format(text)
  a_tag = "<a class='{tag_class}' href='{path}?tag_word={tag}'>{tag}</a>"
  text_with_linking_tag = re.sub(r'(#[^\s]+)', a_tag.format(tag_class='linking_tag', path=path_to_tag_post_list, tag='\\1'), text)
  return mark_safe(text_with_linking_tag)