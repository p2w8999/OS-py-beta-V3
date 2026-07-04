
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import re
import subprocess
import sys
import os
from pathlib import Path


# Language configurations
LANGUAGES = {
    "Python": {
        "extensions": [".py"],
        "keywords": ["def", "class", "if", "else", "for", "while", "import",
                    "from", "return", "True", "False", "None", "try", "except",
                    "finally", "pass", "break", "continue", "raise", "assert",
                    "del", "global", "nonlocal", "and", "or", "not", "in", "is",
                    "lambda", "with", "yield"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "multiline_strings": ['"""', "'''"],
        "functions": r"def\s+(\w+)\s*\(",
        "classes": r"class\s+(\w+)\s*\(",
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000",
        "function_color": "#795e26",
        "class_color": "#267f99"
    },
    "JavaScript": {
        "extensions": [".js", ".jsx", ".mjs", ".cjs"],
        "keywords": ["function", "var", "let", "const", "if", "else", "for",
                    "while", "do", "switch", "case", "break", "continue",
                    "return", "true", "false", "null", "undefined", "try",
                    "catch", "finally", "throw", "class", "extends", "import",
                    "export", "default", "async", "await"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000",
        "function_color": "#795e26"
    },
    "TypeScript": {
        "extensions": [".ts", ".tsx"],
        "keywords": ["function", "var", "let", "const", "if", "else", "for",
                    "while", "do", "switch", "case", "break", "continue",
                    "return", "true", "false", "null", "undefined", "try",
                    "catch", "finally", "throw", "class", "extends", "import",
                    "export", "default", "async", "await", "interface", "type",
                    "enum", "implements", "public", "private", "protected"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000",
        "function_color": "#795e26"
    },
    "HTML": {
        "extensions": [".html", ".htm"],
        "keywords": ["html", "head", "body", "div", "p", "a", "img", "script",
                    "style", "link", "meta", "title", "h1", "h2", "h3", "h4",
                    "h5", "h6", "ul", "ol", "li", "table", "tr", "td", "th"],
        "comments": ["<!--"],
        "strings": ['"', "'"],
        "multiline_comments": [("<!--", "-->")],
        "comment_color": "#808080",
        "tag_color": "#0000ff",
        "string_color": "#008000"
    },
    "CSS": {
        "extensions": [".css"],
        "keywords": ["important", "inherit", "initial", "unset", "auto",
                    "none", "block", "inline", "inline-block", "flex", "grid",
                    "absolute", "relative", "fixed", "sticky", "static"],
        "comments": ["/*"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#ff0000",
        "string_color": "#008000",
        "tag_color": "#800000"
    },
    "SCSS": {
        "extensions": [".scss"],
        "keywords": ["important", "inherit", "initial", "unset", "auto",
                    "none", "block", "inline", "flex", "grid", "mixin", "include"],
        "comments": ["//", "/*"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#ff0000",
        "string_color": "#008000"
    },
    "Sass": {
        "extensions": [".sass"],
        "keywords": ["important", "inherit", "initial", "unset", "auto",
                    "none", "block", "inline", "flex", "grid", "mixin", "include"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#ff0000",
        "string_color": "#008000"
    },
    "Less": {
        "extensions": [".less"],
        "keywords": ["important", "inherit", "initial", "unset", "auto",
                    "none", "block", "inline", "flex", "grid"],
        "comments": ["//", "/*"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#ff0000",
        "string_color": "#008000"
    },
    "Java": {
        "extensions": [".java"],
        "keywords": ["public", "private", "protected", "static", "final",
                    "class", "interface", "extends", "implements", "void",
                    "int", "double", "float", "char", "boolean", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "try", "catch", "finally", "throw", "throws",
                    "new", "this", "super", "import", "package"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "C": {
        "extensions": [".c", ".h"],
        "keywords": ["int", "char", "float", "double", "void", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "struct", "typedef", "enum", "union", "static",
                    "extern", "const", "volatile", "register", "auto"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "C++": {
        "extensions": [".cpp", ".cc", ".cxx", ".hpp", ".hh"],
        "keywords": ["int", "char", "float", "double", "void", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "class", "struct", "typedef", "enum", "union",
                    "static", "extern", "const", "volatile", "public", "private",
                    "protected", "template", "namespace", "using", "std"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "C#": {
        "extensions": [".cs"],
        "keywords": ["public", "private", "protected", "static", "void", "int",
                    "string", "bool", "if", "else", "for", "foreach", "while",
                    "do", "switch", "case", "break", "continue", "return", "class",
                    "struct", "interface", "namespace", "using", "var", "const"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Go": {
        "extensions": [".go"],
        "keywords": ["package", "import", "func", "var", "const", "type", "struct",
                    "interface", "if", "else", "for", "range", "switch", "case",
                    "break", "continue", "return", "go", "defer", "chan", "map"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Rust": {
        "extensions": [".rs"],
        "keywords": ["fn", "let", "mut", "if", "else", "for", "while", "loop",
                    "match", "impl", "trait", "struct", "enum", "pub", "use",
                    "mod", "crate", "self", "super", "return", "break", "continue"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/"), ("/**", "*/"), ("///", "")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Swift": {
        "extensions": [".swift"],
        "keywords": ["func", "var", "let", "if", "else", "for", "while", "repeat",
                    "switch", "case", "break", "continue", "return", "class",
                    "struct", "enum", "protocol", "extension", "import", "guard"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Kotlin": {
        "extensions": [".kt", ".kts"],
        "keywords": ["fun", "val", "var", "if", "else", "for", "while", "when",
                    "class", "data", "object", "interface", "sealed", "import",
                    "package", "return", "break", "continue", "try", "catch",
                    "finally", "throw", "null", "true", "false"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "PHP": {
        "extensions": [".php"],
        "keywords": ["<?php", "?>", "function", "class", "interface", "trait",
                    "if", "else", "for", "foreach", "while", "do", "switch",
                    "case", "break", "continue", "return", "try", "catch",
                    "finally", "throw", "public", "private", "protected", "static",
                    "const", "echo", "print"],
        "comments": ["//", "#"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Ruby": {
        "extensions": [".rb"],
        "keywords": ["def", "class", "module", "if", "else", "elsif", "unless",
                    "for", "while", "until", "each", "do", "end", "begin",
                    "rescue", "ensure", "raise", "return", "break", "next",
                    "true", "false", "nil", "self", "super", "yield"],
        "comments": ["#"],
        "strings": ['"', "'", "`"],
        "multiline_strings": ["=begin", "=end"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Perl": {
        "extensions": [".pl", ".pm"],
        "keywords": ["sub", "my", "our", "local", "if", "else", "elsif", "unless",
                    "for", "foreach", "while", "until", "do", "return", "last",
                    "next", "redo", "use", "require", "package"],
        "comments": ["#"],
        "strings": ['"', "'", "`"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Lua": {
        "extensions": [".lua"],
        "keywords": ["function", "local", "if", "else", "elseif", "then", "end",
                    "for", "while", "do", "repeat", "until", "return", "break",
                    "and", "or", "not", "true", "false", "nil", "in"],
        "comments": ["--"],
        "strings": ['"', "'"],
        "multiline_comments": [("--[[", "]]")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "R": {
        "extensions": [".r"],
        "keywords": ["function", "if", "else", "for", "while", "repeat", "next",
                    "break", "return", "TRUE", "FALSE", "NULL", "NA", "Inf",
                    "NaN", "library", "require", "source"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "MATLAB": {
        "extensions": [".m"],
        "keywords": ["function", "if", "else", "elseif", "end", "for", "while",
                    "switch", "case", "otherwise", "break", "continue", "return",
                    "try", "catch", "global", "persistent"],
        "comments": ["%"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Julia": {
        "extensions": [".jl"],
        "keywords": ["function", "struct", "mutable", "abstract", "type", "if",
                    "else", "elseif", "end", "for", "while", "return", "break",
                    "continue", "try", "catch", "finally", "throw", "using",
                    "import", "export", "const", "let", "local", "global"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "multiline_comments": [("#=", "=#")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Dart": {
        "extensions": [".dart"],
        "keywords": ["void", "int", "double", "String", "bool", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "class", "extends", "implements", "with", "import",
                    "export", "library", "part", "async", "await", "try", "catch",
                    "finally", "throw", "rethrow", "null", "true", "false"],
        "comments": ["//"],
        "strings": ['"', "'", "'''"],
        "multiline_comments": [("/*", "*/"), ("/**", "*/"), ("///", "")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Scala": {
        "extensions": [".scala"],
        "keywords": ["def", "val", "var", "class", "trait", "object", "if", "else",
                    "for", "while", "do", "match", "case", "return", "break",
                    "continue", "try", "catch", "finally", "throw", "import",
                    "package", "implicit", "lazy", "sealed", "abstract", "extends",
                    "with", "new", "this", "super", "null", "true", "false"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Groovy": {
        "extensions": [".groovy"],
        "keywords": ["def", "void", "int", "String", "boolean", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "class", "interface", "trait", "extends", "implements",
                    "import", "package", "try", "catch", "finally", "throw"],
        "comments": ["//"],
        "strings": ['"', "'", "'''"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Objective-C": {
        "extensions": [".m", ".mm"],
        "keywords": ["@interface", "@implementation", "@end", "@property", "@synthesize",
                    "@class", "@public", "@private", "@protected", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "try", "catch", "finally", "throw"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Objective-C++": {
        "extensions": [".mm"],
        "keywords": ["@interface", "@implementation", "@end", "@property", "@synthesize",
                    "@class", "@public", "@private", "@protected", "if", "else",
                    "for", "while", "do", "switch", "case", "break", "continue",
                    "return", "class", "struct", "template", "try", "catch", "finally", "throw"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Visual Basic": {
        "extensions": [".vb"],
        "keywords": ["Sub", "Function", "Class", "Module", "If", "Then", "Else", "ElseIf",
                    "End", "For", "To", "Next", "While", "Do", "Loop", "Select",
                    "Case", "Return", "Exit", "Try", "Catch", "Finally", "Throw"],
        "comments": ["'"],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "F#": {
        "extensions": [".fs"],
        "keywords": ["let", "fun", "function", "if", "then", "else", "for", "in",
                    "do", "while", "match", "with", "type", "class", "struct",
                    "interface", "inherit", "member", "override", "static", "public",
                    "private", "internal", "module", "namespace", "open", "try",
                    "with", "finally", "raise", "true", "false", "null"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("(*", "*)")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Haskell": {
        "extensions": [".hs"],
        "keywords": ["module", "import", "where", "data", "type", "class", "instance",
                    "let", "in", "do", "if", "then", "else", "case", "of",
                    "True", "False", "Just", "Nothing"],
        "comments": ["--"],
        "strings": ['"'],
        "multiline_comments": [("{-", "-}")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "OCaml": {
        "extensions": [".ml", ".mli"],
        "keywords": ["module", "struct", "sig", "end", "type", "let", "rec", "in",
                    "fun", "function", "if", "then", "else", "match", "with",
                    "try", "with", "raise", "true", "false", "Some", "None"],
        "comments": ["(*"],
        "strings": ['"', "'"],
        "multiline_comments": [("(*", "*)")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Elixir": {
        "extensions": [".ex", ".exs"],
        "keywords": ["def", "defmodule", "defp", "defimpl", "defprotocol", "if", "else",
                    "cond", "case", "with", "try", "rescue", "catch", "after",
                    "raise", "throw", "true", "false", "nil", "import", "require",
                    "use", "alias"],
        "comments": ["#"],
        "strings": ['"', "'", "'''"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Erlang": {
        "extensions": [".erl", ".hrl"],
        "keywords": ["-module", "-export", "-import", "-include", "-define", "if",
                    "case", "receive", "after", "fun", "end", "true", "false"],
        "comments": ["%"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Clojure": {
        "extensions": [".clj", ".cljs"],
        "keywords": ["def", "defn", "defmacro", "defrecord", "deftype", "defprotocol",
                    "if", "when", "cond", "case", "let", "fn", "loop", "recur",
                    "try", "catch", "finally", "throw", "require", "use", "import",
                    "ns"],
        "comments": [";;", ";", ";;;", ";;;;"],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Lisp": {
        "extensions": [".lisp", ".lsp"],
        "keywords": ["defun", "defvar", "defparameter", "if", "when", "cond", "case",
                    "let", "let*", "lambda", "loop", "try", "catch", "throw",
                    "require", "use-package", "in-package"],
        "comments": [";;", ";", ";;;", ";;;;"],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Scheme": {
        "extensions": [".scm"],
        "keywords": ["define", "define-syntax", "lambda", "if", "cond", "case", "let",
                    "let*", "letrec", "do", "begin", "set!", "quote", "quasiquote",
                    "unquote", "unquote-splicing"],
        "comments": [";;", ";", ";;;", ";;;;"],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Assembly": {
        "extensions": [".asm", ".s"],
        "keywords": ["mov", "add", "sub", "mul", "div", "and", "or", "xor", "not",
                    "jmp", "je", "jne", "jg", "jl", "jge", "jle", "call", "ret",
                    "push", "pop", "cmp", "inc", "dec", "int"],
        "comments": [";", "#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "SQL": {
        "extensions": [".sql"],
        "keywords": ["SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE",
                    "SET", "DELETE", "CREATE", "TABLE", "ALTER", "DROP", "INDEX",
                    "VIEW", "DATABASE", "JOIN", "INNER", "LEFT", "RIGHT", "OUTER",
                    "ON", "GROUP", "BY", "HAVING", "ORDER", "ASC", "DESC", "AND",
                    "OR", "NOT", "NULL", "PRIMARY", "KEY", "FOREIGN", "REFERENCES"],
        "comments": ["--"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Shell": {
        "extensions": [".sh", ".bash"],
        "keywords": ["if", "then", "else", "elif", "fi", "for", "do", "done", "while",
                    "until", "case", "esac", "function", "local", "export", "readonly",
                    "return", "exit", "source", ".", "true", "false", "null"],
        "comments": ["#"],
        "strings": ['"', "'", "`"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "PowerShell": {
        "extensions": [".ps1", ".psm1"],
        "keywords": ["function", "if", "else", "elseif", "foreach", "for", "while",
                    "do", "until", "switch", "try", "catch", "finally", "throw",
                    "return", "break", "continue", "param", "begin", "process",
                    "end", "exit"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "multiline_comments": [("<#", "#>")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Batch": {
        "extensions": [".bat", ".cmd"],
        "keywords": ["@echo", "echo", "if", "exist", "not", "for", "in", "do", "goto",
                    "call", "set", "setlocal", "endlocal", "exit", "rem"],
        "comments": ["rem", "REM", "::"],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "YAML": {
        "extensions": [".yaml", ".yml"],
        "keywords": [],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "JSON": {
        "extensions": [".json"],
        "keywords": ["true", "false", "null"],
        "comments": [],
        "strings": ['"'],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "XML": {
        "extensions": [".xml"],
        "keywords": [],
        "comments": ["<!--"],
        "strings": ['"', "'"],
        "multiline_comments": [("<!--", "-->")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "TOML": {
        "extensions": [".toml"],
        "keywords": ["true", "false"],
        "comments": ["#"],
        "strings": ['"', "'", "'''"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "INI": {
        "extensions": [".ini"],
        "keywords": [],
        "comments": ["#", ";"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Markdown": {
        "extensions": [".md", ".markdown"],
        "keywords": [],
        "comments": [],
        "strings": [],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "LaTeX": {
        "extensions": [".tex"],
        "keywords": ["\\documentclass", "\\usepackage", "\\begin", "\\end", "\\title",
                    "\\author", "\\date", "\\maketitle", "\\section", "\\subsection",
                    "\\textbf", "\\textit", "\\emph"],
        "comments": ["%"],
        "strings": [],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Dockerfile": {
        "extensions": ["Dockerfile"],
        "keywords": ["FROM", "RUN", "CMD", "ENTRYPOINT", "WORKDIR", "COPY", "ADD",
                    "EXPOSE", "ENV", "ARG", "USER", "VOLUME", "LABEL", "HEALTHCHECK"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Makefile": {
        "extensions": ["Makefile"],
        "keywords": ["all", "clean", "install", "test"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Nginx": {
        "extensions": [".conf"],
        "keywords": ["server", "listen", "server_name", "location", "root", "index",
                    "try_files", "proxy_pass", "upstream", "if", "return", "rewrite"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Apache Config": {
        "extensions": [".htaccess", ".conf"],
        "keywords": ["ServerName", "DocumentRoot", "DirectoryIndex", "RewriteEngine",
                    "RewriteRule", "RewriteCond", "Options", "AllowOverride",
                    "Require", "all", "granted"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Vim Script": {
        "extensions": [".vim"],
        "keywords": ["let", "set", "map", "noremap", "function", "endfunction", "if",
                    "else", "endif", "for", "in", "do", " endfor", "try", "catch",
                    "finally", "endtry", "call"],
        "comments": ['"'],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Zig": {
        "extensions": [".zig"],
        "keywords": ["const", "var", "fn", "if", "else", "for", "while", "switch",
                    "return", "break", "continue", "try", "catch", "throw", "defer",
                    "errdefer", "struct", "enum", "union", "usingnamespace", "pub",
                    "extern", "export", "inline", "comptime"],
        "comments": ["//"],
        "strings": ['"', "'", "'''"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Nim": {
        "extensions": [".nim"],
        "keywords": ["proc", "func", "method", "template", "macro", "type", "var",
                    "const", "let", "if", "elif", "else", "when", "case", "of",
                    "for", "while", "do", "return", "break", "continue", "try",
                    "except", "finally", "raise", "import", "from", "as", "export",
                    "module"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "multiline_comments": [("#[", "]#")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Crystal": {
        "extensions": [".cr"],
        "keywords": ["def", "class", "module", "struct", "alias", "if", "else",
                    "elsif", "case", "when", "then", "end", "for", "while",
                    "until", "do", "return", "break", "next", "begin", "rescue",
                    "ensure", "raise", "true", "false", "nil", "require", "include"],
        "comments": ["#"],
        "strings": ['"', "'", "'''"],
        "multiline_comments": [("=begin", "=end")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "V": {
        "extensions": [".v"],
        "keywords": ["fn", "struct", "interface", "type", "const", "mut", "if", "else",
                    "for", "while", "match", "case", "return", "break", "continue",
                    "import", "module", "pub", "true", "false", "none"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Fortran": {
        "extensions": [".f", ".f90", ".f95"],
        "keywords": ["program", "end", "subroutine", "function", "module", "use",
                    "implicit", "none", "integer", "real", "double", "precision",
                    "complex", "character", "logical", "if", "then", "else", "endif",
                    "do", "enddo", "cycle", "exit", "select", "case", "endselect",
                    "write", "read", "print"],
        "comments": ["!", "C"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "COBOL": {
        "extensions": [".cob", ".cbl"],
        "keywords": ["IDENTIFICATION", "DIVISION", "PROGRAM-ID", "ENVIRONMENT",
                    "DATA", "WORKING-STORAGE", "SECTION", "PROCEDURE", "DISPLAY",
                    "ACCEPT", "IF", "THEN", "ELSE", "END-IF", "PERFORM", "UNTIL",
                    "VARYING", "GO", "TO", "STOP", "RUN"],
        "comments": ["*", "/"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Ada": {
        "extensions": [".adb", ".ads"],
        "keywords": ["procedure", "function", "package", "body", "is", "begin", "end",
                    "if", "then", "else", "elsif", "end if", "for", "loop",
                    "while", "end loop", "case", "when", "end case", "declare",
                    "type", "constant", "variable", "integer", "float", "string",
                    "boolean", "true", "false", "null", "return", "raise"],
        "comments": ["--"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Pascal": {
        "extensions": [".pas"],
        "keywords": ["program", "uses", "begin", "end", "procedure", "function", "var",
                    "const", "type", "if", "then", "else", "for", "to", "downto",
                    "do", "while", "do", "repeat", "until", "case", "of", "break",
                    "continue", "exit", "true", "false", "integer", "real", "string",
                    "boolean", "char"],
        "comments": ["//", "{", "(*"],
        "strings": ['"', "'"],
        "multiline_comments": [("(*", "*)"), ("{", "}")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Delphi": {
        "extensions": [".pas"],
        "keywords": ["program", "unit", "uses", "interface", "implementation", "begin",
                    "end", "procedure", "function", "var", "const", "type", "class",
                    "private", "public", "protected", "published", "if", "then",
                    "else", "for", "to", "downto", "do", "while", "do", "repeat",
                    "until", "case", "of", "try", "finally", "except", "on", "end",
                    "raise"],
        "comments": ["//", "{", "(*"],
        "strings": ['"', "'"],
        "multiline_comments": [("(*", "*)"), ("{", "}")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Prolog": {
        "extensions": [".pl"],
        "keywords": [],
        "comments": ["%"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Solidity": {
        "extensions": [".sol"],
        "keywords": ["contract", "library", "interface", "function", "modifier", "event",
                    "struct", "enum", "mapping", "address", "uint", "int", "bool",
                    "string", "bytes", "if", "else", "for", "while", "do", "break",
                    "continue", "return", "throw", "require", "assert", "revert",
                    "emit", "public", "private", "internal", "external", "view",
                    "pure", "payable"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/"), ("/**", "*/"), ("///", "")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Move": {
        "extensions": [".move"],
        "keywords": ["module", "script", "fun", "struct", "public", "friend", "let",
                    "if", "else", "while", "loop", "return", "break", "continue",
                    "assert", "true", "false", "move", "copy", "borrow", "global",
                    "exists", "acquires"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "GraphQL": {
        "extensions": [".graphql", ".gql"],
        "keywords": ["query", "mutation", "subscription", "type", "interface", "enum",
                    "scalar", "input", "union", "fragment", "on", "extend", "schema",
                    "directive", "field"],
        "comments": ["#"],
        "strings": ['"', "'"],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Protocol Buffers": {
        "extensions": [".proto"],
        "keywords": ["syntax", "package", "import", "option", "message", "enum",
                    "service", "rpc", "returns", "optional", "repeated", "required",
                    "double", "float", "int32", "int64", "uint32", "uint64",
                    "sint32", "sint64", "fixed32", "fixed64", "sfixed32", "sfixed64",
                    "bool", "string", "bytes"],
        "comments": ["//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "HCL (Terraform)": {
        "extensions": [".tf", ".tfvars"],
        "keywords": ["resource", "provider", "variable", "output", "module", "data",
                    "locals", "terraform", "backend", "provisioner", "connection"],
        "comments": ["#", "//"],
        "strings": ['"', "'"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Vue": {
        "extensions": [".vue"],
        "keywords": ["template", "script", "style", "export", "default", "import",
                    "from", "components", "props", "data", "computed", "methods",
                    "watch", "created", "mounted"],
        "comments": ["//", "<!--"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/"), ("<!--", "-->")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Svelte": {
        "extensions": [".svelte"],
        "keywords": ["script", "style", "export", "let", "const", "if", "else", "each",
                    "await", "then", "catch", "import", "from"],
        "comments": ["//", "<!--"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/"), ("<!--", "-->")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "Astro": {
        "extensions": [".astro"],
        "keywords": ["---", "layout", "import", "export", "let", "const", "if", "else"],
        "comments": ["<!--"],
        "strings": ['"', "'"],
        "multiline_comments": [("<!--", "-->")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "JSX": {
        "extensions": [".jsx"],
        "keywords": ["function", "var", "let", "const", "if", "else", "for",
                    "while", "do", "switch", "case", "break", "continue",
                    "return", "true", "false", "null", "undefined", "try",
                    "catch", "finally", "throw", "class", "extends", "import",
                    "export", "default", "async", "await"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "TSX": {
        "extensions": [".tsx"],
        "keywords": ["function", "var", "let", "const", "if", "else", "for",
                    "while", "do", "switch", "case", "break", "continue",
                    "return", "true", "false", "null", "undefined", "try",
                    "catch", "finally", "throw", "class", "extends", "import",
                    "export", "default", "async", "await", "interface", "type",
                    "enum", "implements", "public", "private", "protected"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "React Native": {
        "extensions": [".js", ".jsx", ".tsx"],
        "keywords": ["import", "from", "export", "default", "function", "const", "let",
                    "var", "if", "else", "for", "while", "do", "switch", "case",
                    "break", "continue", "return", "try", "catch", "finally", "throw",
                    "class", "extends", "async", "await", "true", "false", "null",
                    "undefined"],
        "comments": ["//"],
        "strings": ['"', "'", "`"],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "GLSL": {
        "extensions": [".glsl", ".vert", ".frag"],
        "keywords": ["void", "main", "in", "out", "uniform", "attribute", "varying",
                    "vec2", "vec3", "vec4", "mat2", "mat3", "mat4", "float", "int",
                    "bool", "true", "false", "if", "else", "for", "while", "do",
                    "return", "break", "continue", "gl_Position", "gl_FragColor"],
        "comments": ["//"],
        "strings": [],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    },
    "WGSL": {
        "extensions": [".wgsl"],
        "keywords": ["fn", "var", "let", "const", "struct", "if", "else", "for", "loop",
                    "while", "return", "break", "continue", "true", "false", "fn", "vertex",
                    "fragment", "compute", "binding", "group", "location", "in", "out"],
        "comments": ["//"],
        "strings": [],
        "multiline_comments": [("/*", "*/")],
        "comment_color": "#808080",
        "keyword_color": "#0000ff",
        "string_color": "#008000"
    }
}


class TextEditor:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("PyIDE")
        self.window.geometry("1100x800")
        self.current_file = None
        self.current_language = "Python"
        self.plugins = []

        self.create_menu()
        self.create_widgets()
        self.load_plugins()
        self.update_line_numbers()

    def create_menu(self):
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=lambda: self.text_area.edit_undo(), accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo", command=lambda: self.text_area.edit_redo(), accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        editmenu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        editmenu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        menubar.add_cascade(label="Edit", menu=editmenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Run", command=self.run_code, accelerator="F5")
        menubar.add_cascade(label="Run", menu=runmenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        # Language selector
        self.language_var = tk.StringVar(value=self.current_language)
        langmenu = tk.Menu(viewmenu, tearoff=0)
        for lang in LANGUAGES:
            langmenu.add_radiobutton(label=lang, variable=self.language_var,
                                     value=lang, command=self.change_language)
        viewmenu.add_cascade(label="Language", menu=langmenu)
        menubar.add_cascade(label="View", menu=viewmenu)

        pluginsmenu = tk.Menu(menubar, tearoff=0)
        pluginsmenu.add_command(label="Add Plugin", command=self.add_plugin)
        pluginsmenu.add_separator()
        self.plugins_menu = pluginsmenu
        menubar.add_cascade(label="Plugins", menu=pluginsmenu)

        self.window.config(menu=menubar)

        # Bind keyboard shortcuts
        self.window.bind("<Control-n>", lambda e: self.new_file())
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_file())
        self.window.bind("<Control-z>", lambda e: self.text_area.edit_undo())
        self.window.bind("<Control-y>", lambda e: self.text_area.edit_redo())
        self.window.bind("<F5>", lambda e: self.run_code())

    def create_widgets(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Top toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=5)
        ttk.Label(toolbar, text="Language:").pack(side=tk.LEFT, padx=5)
        self.lang_combo = ttk.Combobox(toolbar, values=list(LANGUAGES.keys()),
                                      textvariable=self.language_var, state="readonly")
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self.change_language())

        # Line numbers
        self.line_numbers = tk.Text(main_frame, width=6, padx=3, takefocus=0, border=0,
                                    background='#f0f0f0', foreground='#444',
                                    state='disabled', font=("Consolas", 10))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area = tk.Text(main_frame, wrap="word", font=("Consolas", 10),
                                 undo=True, maxundo=-1, padx=5, pady=5)
        self.text_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL,
                                   command=self.scroll_both)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=self.on_textarea)
        self.line_numbers.configure(yscrollcommand=self.on_linenumber_yview)

        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.text_area.bind("<Configure>", self.on_configure)

        # Output window
        self.output_frame = ttk.Frame(self.window)
        self.output_label = ttk.Label(self.output_frame, text="Output:")
        self.output_label.pack(anchor=tk.W)
        self.output_text = tk.Text(self.output_frame, height=12, font=("Consolas", 9),
                                  bg="#1e1e1e", fg="#d4d4d4", insertbackground="#ffffff")
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

    def scroll_both(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def on_textarea(self, *args):
        self.line_numbers.yview_moveto(args[0])
        self.scroll_both("moveto", args[0])

    def on_linenumber_yview(self, *args):
        self.text_area.yview_moveto(args[0])
        self.scroll_both("moveto", args[0])

    def on_configure(self, event=None):
        self.update_line_numbers()

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()

    def update_line_numbers(self):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        line_count = self.text_area.get("1.0", tk.END).count("\n")
        line_numbers_str = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.config(state=tk.DISABLED)

    def change_language(self):
        self.current_language = self.language_var.get()
        self.highlight_syntax()

    def detect_language(self, file_path):
        ext = Path(file_path).suffix.lower()
        for lang, config in LANGUAGES.items():
            if ext in config["extensions"]:
                return lang
        return "Python"

    def highlight_syntax(self, event=None):
        config = LANGUAGES[self.current_language]
        # Remove all tags
        for tag in self.text_area.tag_names():
            self.text_area.tag_remove(tag, "1.0", tk.END)

        # Highlight keywords
        if "keywords" in config:
            for word in config["keywords"]:
                start_idx = "1.0"
                while True:
                    start_idx = self.text_area.search(r"\b" + re.escape(word) + r"\b",
                                                    start_idx, stopindex=tk.END)
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(word)}c"
                    self.text_area.tag_add("keyword", start_idx, end_idx)
                    start_idx = end_idx
            self.text_area.tag_config("keyword", foreground=config.get("keyword_color", "#0000ff"),
                                    font=("Consolas", 10, "bold"))

        # Highlight strings
        if "strings" in config:
            for quote in config["strings"]:
                start_idx = "1.0"
                while True:
                    pattern = quote + r"[^" + quote + r"]*" + quote
                    start_idx = self.text_area.search(pattern, start_idx,
                                                    stopindex=tk.END, regexp=True)
                    if not start_idx:
                        break
                    end_idx = self.text_area.index(f"{start_idx}+1c")
                    while True:
                        char = self.text_area.get(end_idx)
                        if char == quote or not char:
                            break
                        end_idx = self.text_area.index(f"{end_idx}+1c")
                    if char == quote:
                        end_idx = self.text_area.index(f"{end_idx}+1c")
                    self.text_area.tag_add("string", start_idx, end_idx)
                    start_idx = end_idx
            self.text_area.tag_config("string", foreground=config.get("string_color", "#008000"))

        # Highlight comments
        if "comments" in config:
            for comment in config["comments"]:
                if len(comment) == 1:  # Single line
                    start_idx = "1.0"
                    while True:
                        start_idx = self.text_area.search(re.escape(comment) + r".*$",
                                                        start_idx, stopindex=tk.END, regexp=True)
                        if not start_idx:
                            break
                        end_idx = f"{start_idx} lineend"
                        self.text_area.tag_add("comment", start_idx, end_idx)
                        start_idx = end_idx
            self.text_area.tag_config("comment", foreground=config.get("comment_color", "#808080"))

        # Highlight multiline comments
        if "multiline_comments" in config:
            for (start, end) in config["multiline_comments"]:
                start_idx = "1.0"
                while True:
                    start_idx = self.text_area.search(re.escape(start), start_idx,
                                                    stopindex=tk.END)
                    if not start_idx:
                        break
                    end_idx = self.text_area.search(re.escape(end),
                                                self.text_area.index(f"{start_idx}+{len(start)}c"),
                                                stopindex=tk.END)
                    if end_idx:
                        end_idx = self.text_area.index(f"{end_idx}+{len(end)}c")
                        self.text_area.tag_add("comment", start_idx, end_idx)
                    start_idx = end_idx or "1.0"

        # Highlight functions
        if "functions" in config:
            start_idx = "1.0"
            while True:
                start_idx = self.text_area.search(config["functions"], start_idx,
                                                stopindex=tk.END, regexp=True)
                if not start_idx:
                    break
                start_idx_func = self.text_area.search(r"\w+", start_idx,
                                                    stopindex=tk.END)
                end_idx_func = self.text_area.search(r"\s*\(", start_idx_func,
                                                stopindex=tk.END)
                if start_idx_func and end_idx_func:
                    self.text_area.tag_add("function", start_idx_func, end_idx_func)
                start_idx = end_idx_func
            self.text_area.tag_config("function", foreground=config.get("function_color", "#795e26"))

        # Highlight classes
        if "classes" in config:
            start_idx = "1.0"
            while True:
                start_idx = self.text_area.search(config["classes"], start_idx,
                                                stopindex=tk.END, regexp=True)
                if not start_idx:
                    break
                start_idx_class = self.text_area.search(r"\w+", start_idx,
                                                    stopindex=tk.END)
                end_idx_class = self.text_area.search(r"\s*\(", start_idx_class,
                                                stopindex=tk.END)
                if start_idx_class and end_idx_class:
                    self.text_area.tag_add("class", start_idx_class, end_idx_class)
                start_idx = end_idx_class
            self.text_area.tag_config("class", foreground=config.get("class_color", "#267f99"))

        # Highlight tags (HTML/CSS)
        if "tag_color" in config and self.current_language in ["HTML", "CSS"]:
            if self.current_language == "HTML":
                # HTML tags
                start_idx = "1.0"
                while True:
                    start_idx = self.text_area.search(r"<[^>]+>", start_idx,
                                                    stopindex=tk.END, regexp=True)
                    if not start_idx:
                        break
                    end_idx = self.text_area.search(">", start_idx,
                                                stopindex=tk.END) + "+1c"
                    self.text_area.tag_add("tag", start_idx, end_idx)
                    start_idx = end_idx
            self.text_area.tag_config("tag", foreground=config.get("tag_color", "#800000"))

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.current_language = "Python"
        self.language_var.set("Python")
        self.window.title("PyIDE - New File")
        self.update_line_numbers()

    def open_file(self):
        file_types = [("All Files", "*.*")]
        for lang, config in LANGUAGES.items():
            ext_str = " ".join(f"*{ext}" for ext in config["extensions"])
            file_types.insert(0, (f"{lang} Files", ext_str))
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.current_file = file_path
            self.window.title(f"PyIDE - {file_path}")
            self.current_language = self.detect_language(file_path)
            self.language_var.set(self.current_language)
            self.highlight_syntax()
            self.update_line_numbers()

    def save_file(self):
        if self.current_file:
            content = self.text_area.get("1.0", tk.END)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Success", "File saved!")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_types = [("All Files", "*.*")]
        for lang, config in LANGUAGES.items():
            ext_str = " ".join(f"*{ext}" for ext in config["extensions"])
            file_types.insert(0, (f"{lang} Files", ext_str))
        file_path = filedialog.asksaveasfilename(filetypes=file_types)
        if file_path:
            content = self.text_area.get("1.0", tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.current_file = file_path
            self.window.title(f"PyIDE - {file_path}")
            self.current_language = self.detect_language(file_path)
            self.language_var.set(self.current_language)
            messagebox.showinfo("Success", "File saved!")

    def run_code(self):
        if not self.current_file:
            self.save_file_as()
            if not self.current_file:
                return
        self.save_file()
        self.output_text.delete("1.0", tk.END)
        try:
            if self.current_language == "Python":
                result = subprocess.run(
                    [sys.executable, self.current_file],
                    capture_output=True, text=True,
                    timeout=30
                )
            elif self.current_language == "JavaScript":
                result = subprocess.run(
                    ["node", self.current_file],
                    capture_output=True, text=True,
                    timeout=30
                )
            elif self.current_language == "Java":
                # Compile first
                compile_result = subprocess.run(
                    ["javac", self.current_file],
                    capture_output=True, text=True
                )
                if compile_result.returncode != 0:
                    self.output_text.insert("1.0", compile_result.stderr)
                    return
                class_name = Path(self.current_file).stem
                result = subprocess.run(
                    ["java", class_name],
                    capture_output=True, text=True,
                    timeout=30
                )
            else:
                self.output_text.insert("1.0", f"Cannot run {self.current_language} code yet!")
                return

            output = result.stdout + result.stderr
            self.output_text.insert("1.0", output)
        except subprocess.TimeoutExpired:
            self.output_text.insert("1.0", "Error: Execution timed out!")
        except FileNotFoundError:
            self.output_text.insert("1.0", f"Error: Interpreter for {self.current_language} not found!")
        except Exception as e:
            self.output_text.insert("1.0", f"Error: {str(e)}")

    def load_plugins(self):
        plugin_dir = Path(__file__).parent / "plugins"
        plugin_dir.mkdir(exist_ok=True)
        for file in plugin_dir.glob("*.py"):
            try:
                # Very simple plugin loading for demonstration
                self.plugins.append(str(file))
                self.plugins_menu.add_command(label=file.stem,
                                             command=lambda f=file: self.run_plugin(f))
            except Exception as e:
                print(f"Failed to load plugin {file}: {e}")

    def add_plugin(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Plugins", "*.py")])
        if file_path:
            plugin_dir = Path(__file__).parent / "plugins"
            plugin_dir.mkdir(exist_ok=True)
            dest = plugin_dir / Path(file_path).name
            import shutil
            shutil.copy(file_path, dest)
            self.plugins.append(str(dest))
            self.plugins_menu.add_command(label=Path(dest).stem,
                                         command=lambda f=dest: self.run_plugin(f))
            messagebox.showinfo("Success", "Plugin added!")

    def run_plugin(self, plugin_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "run"):
                    module.run(self)
        except Exception as e:
            messagebox.showerror("Plugin Error", f"Failed to run plugin: {str(e)}")


def open_text_editor(parent):
    TextEditor(parent)
