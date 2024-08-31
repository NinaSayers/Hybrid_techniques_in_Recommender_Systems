from commands.get_user_verctor import GetUserVectorCommand
from commands.test import TfidfFilter
from data_access.db.db import SessionLocal
from data_access.db.repositories import InteractionRepository, ProductRepository
from filters.content_based_filter import ContentBasedFiltering
from models.context_model import Context

# command = GetUserVectorCommand()

session = SessionLocal()
repo = ProductRepository(session)
intrepo = InteractionRepository(session)
all_products =  repo.get_all()

filter = TfidfFilter()

ctx = Context(all_products,'1')

result = filter.apply_filter(ctx)
prId = intrepo.get_interactions_by_user('1')[0].product_id
print(repo.get_by_id(prId).getProductDescribed())
count = 0
for x in result.recommendations:
    
    print(str(x.similarity_score)+ " " + repo.get_by_id(x.product_id).getProductDescribed() + "\n")
    if count > 5: 
        break


# print(repo.get_by_id( "4c69b61db1fc16e7013b43fc926e502d").getProductDescribed() + "\n")

# for p in result: 
#     prod = repo.get_by_id(p[0])
#     print(p[1])
#     print(prod.getProductDescribed() + "\n")



