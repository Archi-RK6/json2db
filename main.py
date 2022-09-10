import os
import sys
import json
from json2db.ModelFactory import CommonModelFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
start_time = time.time()
schemas = ["zakaznar", "zakaznarpod", "zakaznarsog", "zakaznarvoz"]
i = 0
session = []
dir_path = sys.argv[1]
for dir in os.listdir(dir_path):
    print(dir)
    dir_a = '{0}/{1}'.format(dir_path, dir)
    engine = create_engine('postgresql+psycopg2://net_user:net_user_password@80.211.80.219:5432/zit',
                           connect_args={'options': '-csearch_path={}'.format(schemas[i])})
    Session = sessionmaker(bind=engine)
    session.append(Session())
    for file in os.listdir(dir_a):
        print(file)
        with open(f'{dir_path}/{dir}/{file}', encoding='utf-8') as f:
            d = json.load(f)
        factory = CommonModelFactory(is_echo=False, use_foreign_key=True, table_args={'extend_existing': True})
        model = factory.from_json(data=d, root_name="file_r")
        root = model.store(data=d, engine=engine)
        session[i].add(root)
        f.close()
    i += 1
print("До коммитов --- %s seconds ---" % (time.time() - start_time))
for k in range(i):
    session[k].commit()
    session[k].close()
    print("После коммита --- %s seconds ---" % (time.time() - start_time))
