import re


class ContentErrorException(Exception):
    pass


class Toggle(object):
    def __init__(self, url_prefix, content=None, filename=None, match_rules=None, sub_rules=None):
        if not content and not filename:
            raise ContentErrorException("Please pass in some content to transfer")
        elif filename is not None:
            self.filename = filename
            self.content = open(filename).readlines()
        else:
            self.content = content

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

    def parse(self, if_update=False):
        _last = None
        for line in self.content:
            if not if_update and line.startswith(("contents", "Contents")):
                raise ContentErrorException("already has a content")
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
        url_line = "[{}]({})".format(origin_line.strip(), self.url_prefix + "#" + line.strip())
        return self.match_rules[_class] + url_line

    def update(self):
        pass

    def toggle(self):
        if not self.content:
            return self.content
        _contents = self.default_start

        _matched = False
        try:
            for match_line, matcher in self.parse():
                _matched = True
                line = self.format(match_line, matcher)
                _contents.append(line)
        except ContentErrorException as e:
            print(str(e))
            return self.content

        if not _matched:
            return self.content

        _contents.append("\n")
        _contents.extend(self.content)
        return _contents


if __name__ == "__main__":
    toggle = Toggle(filename='./test/test1.md',
                    url_prefix='http://localhost/test.md')
    print(toggle.toggle())



