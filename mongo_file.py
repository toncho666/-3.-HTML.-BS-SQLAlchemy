import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
from pprint import pprint

#импортируем созданный на предыдущем уроке датафрейм с вакансиями SJ и HH
df = pd.read_excel('excel_df.xlsx').drop(['Unnamed: 0'],axis=1)
DF = pd.DataFrame(df)

engine = create_engine('sqlite:///vacancies.db',echo=True)
Base = declarative_base()

class Vacancies(Base):
    __tablename__='vacancies'
    Name = Column(String(255))
    Link = Column(String, primary_key=True, unique=True)
    Main_link = Column(String)
    Employer = Column(String)
    City = Column(String)
    Salary_min = Column(Integer)
    Salary_max = Column(Integer)

    def __init__(self, Name, Link, Main_link, Employer, City, Salary_min, Salary_max):
        self.Name = Name
        self.Link = Link
        self.Main_link = Main_link
        self.Employer = Employer
        self.City = City
        self.Salary_min = Salary_min
        self.Salary_max = Salary_max

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#пробежать по строкам датафрейма можно так.
#for i, row in DF.iterrows():
#    for j, column in row.iteritems():
#        session.add(column)

# импорт датафрейма в базу данных.
DF.to_sql(con=engine, name = 'vacancies', if_exists='replace')

#поиск вакансий с минимальной ЗП больше 100 000 рублей.
sum = 100000
conn = sqlite3.connect('vacancies.db')
cursor = conn.cursor()
cursor.execute(f'SELECT * FROM vacancies WHERE "Salary min" >={sum}')

result = cursor.fetchall()
pprint(result)

conn.close()
session.commit()
session.close()
