from commands.get_user_verctor import GetUserVectorCommand
from data_access.db.db import SessionLocal
from data_access.db.repositories import ProductRepository

command = GetUserVectorCommand()

session = SessionLocal()
repo = ProductRepository(session)

result = command.recommend_products(1,10)

print(repo.get_by_id( "4c69b61db1fc16e7013b43fc926e502d").getProductDescribed() + "\n")

for p in result: 
    prod = repo.get_by_id(p[0])
    print(p[1])
    print(prod.getProductDescribed() + "\n")

