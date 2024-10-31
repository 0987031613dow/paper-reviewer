---
title: {{ paper_title }}
summary: {{ paper_summary }}
categories: ["AI Generated", {% if hf_daily_papers_date_tag %}"🤗 Daily Papers"{% endif %}]
tags: [{% if category %}"{{ category }}",{% endif %} {% if sub_category %}"{{ sub_category }}",{% endif %} {% if affiliation %}"🏢 {{ affiliation }}",{% endif %}]
showSummary: true
date: {{ publish_date }}
draft: false
---

<br>

{% raw %}{{< keywordList >}}{% endraw %}
{% raw %}{{< keyword icon="fingerprint" >}}{% endraw %} {{ arxiv_id }} {% raw %}{{< /keyword >}}{% endraw %}
{% raw %}{{< keyword icon="writer" >}}{% endraw %} {{ author }} {% raw %}{{< /keyword >}}{% endraw %}
{% if hf_daily_papers_date_tag %} 
{% raw %}{{< keyword icon="hf-logo" >}}{% endraw %} {{ hf_daily_papers_date_tag }} {% raw %}{{< /keyword >}}{% endraw %}
{% endif %} 
{% raw %}{{< /keywordList >}}{% endraw %}

{% raw %}{{< button{% endraw %} href="{{ arxiv_url }}"{% raw %} target="_self" >}}{% endraw %}
{% raw %}↗ arXiv{% endraw %}
{% raw %}{{< /button >}}{% endraw %}
&nbsp; 
{% raw %}{{< button{% endraw %} href="{{ hf_url }}"{% raw %} target="_self" >}}{% endraw %}
{% raw %}↗ Hugging Face{% endraw %}
{% raw %}{{< /button >}}{% endraw %}

### TL;DR

{% raw %}
{{< lead >}}
{% endraw %}
{{ tldr }}
{% raw %}
{{< /lead >}}
{% endraw %}

#### Key Takeaways

{% raw %}{{< alert "star" >}}{% endraw %}
{% raw %}{{< typeit speed=10 lifeLike=true >}}{% endraw %} {{ takeaways[0] }} {% raw %}{{< /typeit >}}{% endraw %}
{% raw %}{{< /alert >}}{% endraw %}

{% raw %}{{< alert "star" >}}{% endraw %}
{% raw %}{{< typeit speed=10 startDelay=1000 lifeLike=true >}}{% endraw %} {{ takeaways[1] }} {% raw %}{{< /typeit >}}{% endraw %}
{% raw %}{{< /alert >}}{% endraw %}

{% raw %}{{< alert "star" >}}{% endraw %}
{% raw %}{{< typeit speed=10 startDelay=2000 lifeLike=true >}}{% endraw %} {{ takeaways[2] }} {% raw %}{{< /typeit >}}{% endraw %}
{% raw %}{{< /alert >}}{% endraw %}

#### Why does it matter?
{{ reason_why_matter }}

------
#### Visual Insights

{% if first_figure %}

![]({{ first_figure.figure_path }})

> 🔼 {{ first_figure.description }}
> <details>
> <summary>read the caption</summary>
> {{ first_figure.caption }}
> </details>

{% endif %}

{% if first_chart %}

![]({{ first_chart.figure_path }})

> 🔼 {{ first_chart.description }}
> <details>
> <summary>read the caption</summary>
> {{ first_chart.caption }}
> </details>

{% endif %}

{% if first_table %}

{% raw %}{{< table-caption >}}{% endraw %}
{{ first_table.content }}{% raw %}{{< /table-caption >}}{% endraw %}

> 🔼 {{ first_table.description }}
> <details>
> <summary>read the caption</summary>
> {{ first_table.caption }}
> </details>

{% endif %}

{% if other_figures|length > 1 or other_charts|length > 1 or other_tables|length > 1 %}

### More visual insights
{% if other_figures|length > 1 %}
{% raw %}<details>{% endraw %}
{% raw %}<summary>More on figures{% endraw %}
{% raw %}</summary>{% endraw %}

{% for figure in other_figures %}
![]({{ figure.figure_path }})

> 🔼 {{ figure.description }}
> <details>
> <summary>read the caption</summary>
> {{ figure.caption }}
> </details>


{% endfor %}
{% raw %}</details>{% endraw %}
{% endif %}
{% if other_charts|length > 1 %}

{% raw %}<details>{% endraw %}
{% raw %}<summary>More on charts{% endraw %}
{% raw %}</summary>{% endraw %}

{% for chart in other_charts %}
![]({{ chart.figure_path }})

> 🔼 {{ chart.description }}
> <details>
> <summary>read the caption</summary>
> {{ chart.caption }}
> </details>

{% endfor %}
{% raw %}</details>{% endraw %}
{% endif %}
{% if other_tables|length > 1 %}

{% raw %}<details>{% endraw %}
{% raw %}<summary>More on tables{% endraw %}
{% raw %}</summary>{% endraw %}

{% for table in other_tables %}
{% raw %}{{< table-caption >}}{% endraw %}
{{ table.content }}{% raw %}{{< /table-caption >}}{% endraw %}
> 🔼 {{ table.description }}
> <details>
> <summary>read the caption</summary>
> {{ table.caption }}
> </details>
{% endfor %}
{% raw %}</details>{% endraw %}
{% endif %}

{% endif %}

### Full paper

{% raw %}{{< gallery >}}{% endraw %}{% for paper_img in paper_imgs %}
{% raw %}<img {% endraw %}src="{{ paper_img }}" {% raw %}class="grid-w50 md:grid-w33 xl:grid-w25" />{% endraw %}{% endfor %}
{% raw %}{{< /gallery >}}{% endraw %}
