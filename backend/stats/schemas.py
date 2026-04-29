from pydantic import BaseModel


class TimeBase(BaseModel):
    days: int
    hours: int
    minutes: int

class TimeResponse(BaseModel):
    ...


class StatusAvgTimeBase(BaseModel):
    status_title: str
    avg_duration_sec: float

class StatusAvgTimeResponse(StatusAvgTimeBase):
    ...

class StatusAvgTimeFullBase(BaseModel):
    status_title: str
    days: int
    hours: int
    minutes: int
    avg_duration_sec: float

class StatusAvgTimeFullResponse(StatusAvgTimeFullBase):
    ...


# кто быстрее всех переводит задачи в Done
class ProductiveUsersBase(BaseModel):
    login: str
    completion_time_sec: float

class ProductiveUsersResponse(ProductiveUsersBase):
    ...

class ProductiveUserFullsBase(BaseModel):
    login: str
    days: int
    hours: int
    minutes: int
    completion_time_sec: float

class ProductiveUsersFullResponse(ProductiveUserFullsBase):
    ...