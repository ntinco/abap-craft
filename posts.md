---
layout: default
title: Posts
---

# Posts

Browse all ABAP Craft articles.

<ul>
  {% for post in site.posts %}
    <li>
      <strong><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></strong><br>
      <small>{{ post.date | date: "%Y-%m-%d" }}{% if post.lang %} · Language: {{ post.lang }}{% endif %}</small>
      {% if post.excerpt %}
        <p>{{ post.excerpt | strip_html | truncatewords: 35 }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
