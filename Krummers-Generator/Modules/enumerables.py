import enum as en

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
