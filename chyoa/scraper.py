__all__ = ["Scraper"]

from .parser import ChapterParser
from .story import Chapter, Story
from .util import get_choice_names
import re

CHYOA_URL_REGEX = re.compile(r"^https://chyoa.com/story/[^ ]+\.[0-9]+$")

class Scraper(object):
    def __init__(self, url):
        self.parser = ChapterParser()
        self.url = url
        self.visited = set()
        self.story = None

    def scrape(self):
        self.story = self.parser.get_chapter(self.url)
        self.visited.add(self.url)

        print(self.story)
        if not isinstance(self.story, Story):
            print("The URL you gave points to a chapter, not a full story.")
            exit(1)

        print("Story \"%s\":\nRoot \"%s\":\n%s" % (
            self.story.title, self.story.name, get_choice_names(self.story.choices)))
        for id, url in self.story.choices:
            self._scrape_chapter(url, id)

    def _scrape_chapter(self, url, id):
        if url in self.visited:
            print("(already visited %s)" % url)
            return

        chapter = self.parser.get_chapter(url)
        self.visited.add(url)

        if chapter is None:
            return

        self.story.chapters[id] = chapter
        print("Chapter \"%s\":\n%s" % (chapter.name, get_choice_names(chapter.choices)))
        for id, url in chapter.choices:
            self._scrape_chapter(url, id)

    @staticmethod
    def is_chyoa_url(url):
        return bool(CHYOA_URL_REGEX.fullmatch(url))

