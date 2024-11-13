import enum as en
import typing as tp

class Action(en.Enum):
    Create = en.auto()
    Generate = en.auto()
    Delete = en.auto()
    Exit = en.auto()

class CreateAction(en.Enum):
    Create = en.auto()
    Edit = en.auto()
    Exit = en.auto()

class CreateEditAction(en.Enum):
    Add = en.auto()
    Remove = en.auto()
    Redownload = en.auto()
    Exit = en.auto()

class TrackType(en.Enum):
    Normal = en.auto()
    Wish = en.auto()
    Nintendo = en.auto()
    
    def __lt__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            raise TypeError("unsupported operand type(s) for '<': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.value < other.value
    
    def __le__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            raise TypeError("unsupported operand type(s) for '<=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.value <= other.value
    
    def __eq__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            return False
        
        return self.value == other.value
    
    def __ge__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            raise TypeError("unsupported operand type(s) for '>=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.value >= other.value
    
    def __gt__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            raise TypeError("unsupported operand type(s) for '>': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.value > other.value
    
    def __ne__(self, other: tp.Self) -> bool:
        if not isinstance(other, TrackType):
            return True
        
        return self.value != other.value
