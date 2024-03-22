
SECTIONS = [ "read", "edit", "history" ]
SECTION_NAMES = dict(zip(SECTIONS, ["Read", "Edit", "View History"]))

class SectionTab:
	def __init__(self, href: str, id: str, active: bool) -> None:
		self.href = "#" if active else href
		self.id = id
		self.title = SECTION_NAMES[id]
		self.cls = "active" if active else ""

def get_section_tab(request, article_title, active_section: str,
					force_hide_editor: bool = False,
					force_hide_history: bool = False) -> list[SectionTab]:
	ret = []
	for section in SECTIONS:
		if (not request.user.is_authenticated or force_hide_editor) and section == "edit":
			continue
		if section == "history" and force_hide_history:
			continue
		ret.append(SectionTab(
			"/a/{}/{}".format(article_title, section if section != "read" else ""),
			section, section == active_section
		))
	return ret