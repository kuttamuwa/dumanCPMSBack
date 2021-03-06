from appconfig.errors.cruds import CannotCreate


class DomainCannotCreate(CannotCreate):
    item = "Domain"


class DomainCannotUpdate(CannotCreate):
    item = "Domain"


class DomainCannotRead(CannotCreate):
    item = "Domain"

