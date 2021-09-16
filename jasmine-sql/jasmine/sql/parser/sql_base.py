from antlr4 import Lexer, Parser

# sql_modes
NoMode = 0
AnsiQuotes = 1 << 0
HighNotPrecedence = 1 << 1
PipesAsConcat = 1 << 2
IgnoreSpace = 1 << 3
NoBackslashEscapes = 1 << 4

CHARSETS = {
    "big5",
    "dec8",
    "cp850",
    "hp8",
    "koi8r",
    "latin1",
    "latin2",
    "swe7",
    "ascii",
    "ujis",
    "sjis",
    "hebrew",
    "tis620",
    "euckr",
    "koi8u",
    "gb2312",
    "greek",
    "cp1250",
    "gbk",
    "latin5",
    "armscii8",
    "utf8",
    "ucs2",
    "cp866",
    "keybcs2",
    "macce",
    "macroman",
    "cp852",
    "latin7",
    "utf8mb4",
    "cp1251",
    "utf16",
    "utf16le",
    "cp1256",
    "cp1257",
    "utf32",
    "binary",
    "geostd8",
    "cp932",
    "eucjpms",
    "gb18030",
}


class SQLBaseLexer(Lexer):
    serverVersion = 80000
    inVersionComment = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # [first, second, third], ...
        self.queued_tokens = []

        self.charsets = {f"_{charset.lower()}" for charset in CHARSETS}
        self.sql_mode = NoMode

    def nextToken(self):
        # nextToken may add to self.queued_tokens.
        if not self.queued_tokens:
            self.queued_tokens.append(super().nextToken())

        return self.queued_tokens.pop(0)

    def checkVersion(self, version: str):
        """
        Is the server version >= this version number?
        """
        if len(version) < 8:
            return False

        if int(version[3:]) <= self.serverVersion:
            self.inVersionComment = True
            return True

        return False

    def checkCharset(self, charset: str):
        return self.UNDERSCORE_CHARSET if charset in self.charsets else self.IDENTIFIER

    def isSqlModeActive(self, sql_mode: int) -> bool:
        return bool(self.sql_mode & sql_mode)

    def determineFunction(self, proposed: int):
        if self.isSqlModeActive(IgnoreSpace):
            self.input = self._input.LA(1)
            while self.input in " \t\r\n":
                self._interp.consume(self._input)
                self.channel = self.HIDDEN
                self.type = self.WHITESPACE
                self.input = self._input.LA(1)

        if self._input.LA(1) == "(":
            return proposed
        else:
            return self.IDENTIFIER

    # TODO: Do the fancy version and don't mangle concat-strings.
    def getText(self) -> str:
        return self._interp.getText(self._input)

    def determineNumericType(self, value):
        # TODO: Parse this properly.
        return self.LONG_NUMBER

    def emitDot(self):
        dot_token = self._factory.create(
            (self, self._input),
            self.DOT_SYMBOL,
            self._text,
            self._channel,
            self._tokenStartCharIndex,
            self._tokenStartCharIndex,
            self._tokenStartLine,
            self._tokenStartColumn,
        )
        self.queued_tokens.append(dot_token)
        self._tokenStartCharIndex += 1


class SQLBaseParser(Parser):
    serverVersion = 80000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sql_mode = NoMode

    def isSqlModeActive(self, sql_mode: int) -> bool:
        return bool(self.sql_mode & sql_mode)
