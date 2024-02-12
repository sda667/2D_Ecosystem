from abc import ABC, abstractmethod
class Case(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = "NONE"
    
    @property
    def case_type(self) -> str:
        return self.name

class SurfaceSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Surface Sea"

class CaseSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sea"

class DeepSea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deep Sea"

class Sand(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sand"

class Land(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Land"

class FishingArea(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Finshing Area"

class CaseCoral(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Coral"

class Volcano(Case):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Volcano"