import os
import json
from sqlalchemy import create_engine
from json2db.ModelFactory import CommonModelFactory

schemas = ["zakaznarpod", "zakaznarsog", "zakaznarvoz", "zakaznar"]
i = 0
dir_path = 'pattern'
for file in os.listdir(dir_path):
    print(file)
    with open(f'{dir_path}/{file}', encoding='utf-8') as f:
        d = json.load(f)
    engine = create_engine('postgresql+psycopg2://net_user:net_user_password@80.211.80.219:5432/zit',
                           connect_args={'options': '-csearch_path={}'.format(schemas[i])})
    factory = CommonModelFactory(is_echo=False, use_foreign_key=True, table_args={'extend_existing': True})
    model = factory.from_json(data=d, root_name="file_r")
    model.delete_tables_in_db(engine=engine)  # удаление
    i += 1
