

class Field:
    def __init__(self, name: str, comment: str = ""):
        self._name = name
        self.comment = comment

    @property
    def name(self) -> str:
        return self._name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value.replace('\n', ' ')

    def __str__(self):
        param = self._name.split('.')[-1]
        return f"{param}: {self._comment}"


class Message:
    def __init__(self, name: str):
        self._name = name
        self._comment = None
        self._fields = []

    def add_field(self, field: Field):
        self._fields.append(field)

    @property
    def name(self) -> str:
        return self._name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    def __str__(self):
        result = ""
        if self._comment:
            result += f"{self._comment}\n"
        if self._fields:
            result += f"\nArguments:\n{self._arguments()}\n"
        return result

    def _arguments(self) -> str:
        return "\n".join(f"    {field}" for field in self._fields)
