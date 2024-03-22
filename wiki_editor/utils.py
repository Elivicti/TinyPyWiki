from markdown import markdown
from bs4 import BeautifulSoup, Tag
# from django.core.exceptions import ValidationError

from django.utils import timezone
from datetime import datetime

def make_formatted_time(time: datetime | None = None, fmt: str = "%Y-%m-%d, at %H:%M:%S (%Z)"):
	if time is None:
		time = timezone.now()
	return time.strftime(fmt)

class WikiArticle:
	def __init__(self, title: str = "", intro: str = "", contents_panel: str = "", article: str = "") -> None:
		self.title = title
		self.intro = intro
		self.contents_panel = contents_panel
		self.article = article

	def __str__(self) -> str:
		return self.title + self.intro + self.contents_panel + self.article

def get_article_title(markdown_content: str, features: str = "html.parser") -> str:
	html = BeautifulSoup(markdown(markdown_content), features=features)
	title = html.find("h1")
	if title:
		return title.get_text()
	raise ValueError("This article does not have a title.")

def parse_markdown(markdown_content: str, features: str = "html.parser"):
	html = BeautifulSoup(markdown(markdown_content), features=features)
	title = html.find("h1")
	# downgrade other h1 to h2
	for h1 in title.find_all_next("h1"):
		h2 = html.new_tag("h2", attrs=h1.attrs)
		h2.string = h1.get_text()
		h1.replace_with(h2)

	# create contents panel
	contents_panel = BeautifulSoup(features=features)
	div_contentsPanel = contents_panel.new_tag("div", attrs={"class" : "contentsPanel"})
	div_contentsHeader = contents_panel.new_tag("div", attrs={"class" : "contentsHeader"})
	div_contentsHeader.string = "Content"
	div_contentsPanel.append(div_contentsHeader)
	def make_contents_panel(elem: Tag, root: Tag, index: int = 2, root_id: str = ""):
		parent_elem = elem
		header_tag = f"h{index}"
		id = 1
		while True:
			elem = elem.find_next(header_tag)
			if elem is None or elem.find_previous("h%d" % (index - 1)) is not parent_elem:
				break
			li = contents_panel.new_tag("li")
			span = contents_panel.new_tag("span")
			span.string = "%s%d" % (root_id, id)
			a = contents_panel.new_tag("a", attrs={"href": "#" + elem.text})
			a.string = elem.text
			li.append(span)
			li.append(a)
			elem.attrs["id"] = elem.text

			sub_h_tag = elem.find_next("h%d" % (index + 1))
			if sub_h_tag is not None and sub_h_tag.find_previous(header_tag) is elem:
				sub_ul = make_contents_panel(
					elem, contents_panel.new_tag("ul", attrs={"class" : "contents-ul"}),
					index + 1, span.string + "."
				)
				li.append(sub_ul)
			root.append(li)
			id += 1
		return root
	ul = make_contents_panel(title, contents_panel.new_tag("ul", attrs={"class" : "contents-ul"}))
	div_contentsPanel.append(ul)
	contents_panel.append(div_contentsPanel)
	# html.find("h2").insert_before(contents_panel)

	# split html into title, intro, contents and article part
	wiki = WikiArticle(title=title.string)
	for tag in title.next_siblings:
		if (tag.name == "h2"):
			break
		wiki.intro += str(tag)
	wiki.contents_panel = str(contents_panel)

	first_h2 = html.find("h2")
	wiki.article += str(first_h2)

	for tag in first_h2.next_siblings:
		wiki.article += str(tag)

	return wiki

def find_in_markdown(hint: str, markdown_content: str, features: str = "html.parser" ):
	html = BeautifulSoup(markdown(markdown_content), features=features)
	if hint not in html.get_text():
		return None
	first_p = html.find("p")
	intro = first_p.get_text()
	if len(intro) >= 30:
		intro = intro[:30] + " ..."
	return intro
	
	