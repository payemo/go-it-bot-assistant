class Tag:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, value: object) -> bool:
        return self.name == value
