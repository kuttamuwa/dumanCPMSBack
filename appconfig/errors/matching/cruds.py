from appconfig.errors.cruds import CannotCreate


class MatchingCannotCreate(CannotCreate):
    item = "Matching"


class MatchingCannotUpdate(CannotCreate):
    item = "Matching"


class MatchingCannotRead(CannotCreate):
    item = "Matching"

