from sqlalchemy.orm import sessionmaker

from my_scraper.models import Authors, Quotes, db_connect, create_table


class MyScraperPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        author_data = Authors()
        quotes_data = Quotes()
        author_data.name = item['name']
        author_data.author_link = item['author_link']
        quotes_data.tags = item['tags']
        quotes_data.quote_content = item['quotes']

        exist_author = session.query(Authors).filter_by(name=author_data.name).first()
        if exist_author:
            quotes_data.authors = exist_author
        else:
            quotes_data.authors = author_data

        try:
            session.add(quotes_data)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
