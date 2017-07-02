import re


class ContentErrorException(Exception):
    pass


def next_no_blank(contents):
    for index, single_line in enumerate(contents):
        if single_line.strip():
            return index


def next_blank(contents):
    for index, single_line in enumerate(contents):
        if not single_line.strip():
            return index


class Toggle(object):
    def __init__(self, url_prefix, content=None, filename=None, match_rules=None, sub_rules=None):
        if not content and not filename:
            raise ContentErrorException("Please pass in some content to transfer")
        elif content is not None:
            self.content = content
        else:
            self.filename = filename
            self.content = open(filename).readlines()

        self.url_prefix = url_prefix
        self.sub_rules = sub_rules or {
                " ": "-",
                "/": "",
                "\.": "",  # 正则表达式字符需要转义
                "[A-Z]": "lambda x: x.group().lower()"  # 转换成小写
        }
        self.match_rules = match_rules or {
            "===": "- ",
            '---': "  - "
        }
        self.default_start = ["Contents\n", "===\n", "\n"]

    def parse(self, contents):
        _last = None
        for line in contents:
            if line.startswith(tuple(self.match_rules.keys())):
                # 匹配到了,但是没有_last或者_last为空则报错
                if not _last or not _last.strip():
                    raise ContentErrorException("Markdown Content maybe wrong!")
                yield _last, line[:3]
            _last = line

    def format(self, line, _class):
        origin_line = line
        for match, repl in self.sub_rules.items():
            line = re.sub(match, eval(repl) if repl.startswith("lambda") else repl, line)
        url_line = "[{}]({})\n".format(origin_line.strip(), self.url_prefix + "#" + line.strip())
        return self.match_rules[_class] + url_line

    def update(self):

        content_start = next_no_blank(self.content)
        if self.content[content_start] != self.default_start[0]:
            print("didn't find a content to update")

        real_content_start = next_no_blank(self.content[content_start + 2:]) + content_start + 1
        real_content_end = next_blank(self.content[real_content_start + 1:]) + real_content_start + 1

        body_start = next_no_blank(self.content[real_content_end + 1:]) + real_content_end + 1

        body = self.content[body_start:]
        contents = self._toggle(body)
        contents.extend(body)
        return contents

    def generate(self):
        contents = self._toggle(self.content)
        contents.extend(self.content)
        return contents

    def _toggle(self, contents=None):
        if not contents:
            print("data is empty")
            return []

        if contents[0] == self.default_start[0]:
            print("already has a content")
            return []

        _contents = self.default_start

        _matched = False
        try:
            for match_line, matcher in self.parse(contents):
                _matched = True
                line = self.format(match_line, matcher)
                _contents.append(line)
        except ContentErrorException as e:
            print(str(e))
            return []

        if not _matched:
            return []

        _contents.append("\n")
        return _contents


if __name__ == "__main__":
    toggle = Toggle(filename='./README.md',
                    url_prefix='https://github.com/Microndgt/toggle')
    print(''.join(toggle.update()))



