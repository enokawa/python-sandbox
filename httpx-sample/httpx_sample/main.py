import httpx
from pydantic import BaseModel


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company


def main():
    r = httpx.get("https://jsonplaceholder.typicode.com/users/1")
    r_json = r.json()
    user = User(**r_json)
    print(user.company.name)  # => Romaguera-Crona


if __name__ == "__main__":
    main()
