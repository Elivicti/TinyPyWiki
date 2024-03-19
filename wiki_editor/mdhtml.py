from markdown import markdown
from bs4 import BeautifulSoup, Tag
from typing import TextIO

class WikiArticle:
	def __init__(self, title: str = "", intro: str = "", contents_panel: str = "", article: str = "") -> None:
		self.title = title
		self.intro = intro
		self.contents_panel = contents_panel
		self.article = article

	def __str__(self) -> str:
		return self.title + self.intro + self.contents_panel + self.article

def parse_markdown(file: TextIO, features: str = "html.parser"):
	html = BeautifulSoup(markdown(file.read()), features=features)
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
		header_tag = f"h{index}"
		id = 1
		while True:
			elem = elem.find_next(header_tag)
			if elem is None:
				break
			li = contents_panel.new_tag("li")
			span = contents_panel.new_tag("span")
			span.string = "%s%d" % (root_id, id)
			a = contents_panel.new_tag("a", attrs={"href": "#" + elem.text})
			a.string = elem.text
			li.append(span)
			li.append(a)
			elem.attrs["id"] = elem.text

			if elem.find_next("h%d" % (index + 1)) is not None:
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
