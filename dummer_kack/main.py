class Student:
    def __init__(self, student_data: dict):
        self.name: str | None = student_data.get('name')
        self.motivation: int | None = student_data.get('motivation')

    def __cmp__(self, other) -> int:
        if self.motivation < other.motivation:
            return -1
        elif self.motivation > other.motivation:
            return 1
        else:
            return 0

    def is_motivated(self) -> bool:
        return True if self.motivation > 5 else False

    def get_motivation(self) -> str:
        return f'''{self.name} hat{' ' if self.get_motivation() else ' keinen '}Bock.'''

    def cmp_motivation(self, other):
        match(self.__cmp__(other)):
            case 1:
                return f'''{self.name} ist motivierter als {other.name}.'''
            case 0:
                return f'''{self.name} und {other.name} sind beide gleich motiviert.'''
            case -1:
                return f'''{self.name} ist nicht so motiviert wie {other.name}.'''
            case _:
                return f'''Was geht hier ab?!'''
