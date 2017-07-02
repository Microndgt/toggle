Contents
===

- [Usage](https://github.com/Microndgt/toggle#usage)
  - [QuickStart](https://github.com/Microndgt/toggle#quickstart)
  - [arguments of Toggle](https://github.com/Microndgt/toggle#arguments-of-toggle)
- [Author](https://github.com/Microndgt/toggle#author)

# toggle
generate and update markdown table of contents on the top of md file

![](https://img.shields.io/badge/Python-3.5-green.svg)

Usage
=====

QuickStart
---

```
t = Toggle(filename="path/to/file", url_prefix="content/url/prefix")
# 生成目录
t.generate()  # return contents of md
# 更新目录
t.update()  # return contents of md
```

arguments of Toggle
-------------------

- url_prefix: 该md显示网页的url
- filename: 输入为文件路径
- content: 输入为文件内容数据,list,每一项为文件数据的一行,若同时输入文件名和文件数据,以文件数据优先
- match_rules: 匹配规则,dict,默认匹配 === 和 ---,值为该匹配项对应生成的md目录行的前缀,如===对应`- `
- sub_rules: 替换规则,dict以替换标题项中的字符,使得符合markdown解析规则,比如替换'.'为''

Example
=======

本文就是自动生成目录的一个例子

Author
======

[SkyRover](http://skyrover.me)