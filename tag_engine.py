class TagEngine:
    def __init__(self, tags_input):
        self.tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    def has_tag(self, tag):
        return tag in self.tags

    def any_known_tag_owner(self, people):
        for tag in self.tags:
            for p in people:
                if p.tag == tag:
                    return p
        return None
