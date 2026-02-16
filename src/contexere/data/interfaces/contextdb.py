import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData, Table
from sqlalchemy import  exists, and_, create_engine, inspect, insert, select
from sqlalchemy.exc import IntegrityError

from contexere import conf

rag_id_length = conf.__MAX_PROJECT_ID_LENGTH__ + 5  # year 2, month 1, day 1, enumerator 1
metadata = MetaData()

projects = Table('Project', metadata,
                 Column('ID', Integer(), primary_key=True, autoincrement=True),
                 Column('Name', String(conf.__MAX_PROJECT_ID_LENGTH__), unique=True, nullable=False),
                 Column('Description', String(255)),
                 )

researcher = Table('Researcher', metadata,
                 Column('ID', Integer(), primary_key=True, autoincrement=True),
                 Column('Name', String(conf.__MAX_RESEARCHER_NAME_LENGTH__), unique=True, nullable=False),
                 Column('Email', String(255)),
                 )

research_artefact_groups = Table('RAG', metadata,
                                 Column('ID', String(rag_id_length), primary_key=True),
                                 Column('Project', ForeignKey('Project.Name'), nullable=False),
                                 Column('Date', String(4), nullable=False),
                                 Column('Step', String(1), nullable=False),
                                 Column('ResearcherID', ForeignKey('Researcher.ID'), nullable=False),
                                 )

research_knowledge_graph = Table('KnowledgeGraph', metadata,
                                 Column('ID', Integer(), primary_key=True, autoincrement=True),
                                 Column('Parent', ForeignKey('RAG.ID'), nullable=False),
                                 Column('Child', ForeignKey('RAG.ID'), nullable=False),
                                 )

research_artefact_paths = Table('Path', metadata,
                                Column('ID', Integer(), primary_key=True, autoincrement=True),
                                Column('Name', String(conf.__MAX_PATH_LENGTH_BYTES__), nullable=False),
                                )

research_artefacts = Table('Artefact', metadata,
                           Column('ID', Integer(), primary_key=True, autoincrement=True),
                           Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                           Column('FileName', String(conf.__MAX_FILENAME_LENGTH_BYTES__), nullable=False),
                           Column('FileExtension', String(conf.__MAX_FILE_EXTENSION_LENGTH_BYTES__), nullable=False),
                           Column('Path', ForeignKey('Path.ID'), nullable=False),
                           Column('IsGenerator', Boolean(), default=False),
                           Column('IsDirectory', Boolean(), default=False),
                           )

research_artefacts = Table('MarkupFile', metadata,
                           Column('ID', Integer(), primary_key=True, autoincrement=True),
                           Column('FileName', String(conf.__MAX_FILENAME_LENGTH_BYTES__), nullable=False),
                           Column('FileExtension', String(conf.__MAX_FILE_EXTENSION_LENGTH_BYTES__), nullable=False),
                           Column('Path', ForeignKey('Path.ID'), nullable=False),
                           )

research_notes = Table('Note', metadata,
                       Column('ID', Integer(), primary_key=True, autoincrement=True),
                       Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                       Column('File', ForeignKey('MarkupFile.ID'), nullable=False),
                       Column('Quote', String(conf.__MAX_QUOTE_LENGTH__), nullable=False),
                       Column('LineNr', Integer(), nullable=False),
                       )

keywords = Table('Keyword', metadata,
                 Column('ID', Integer(), primary_key=True, autoincrement=True),
                 Column('Keyword', String(conf.__MAX_KEYWORD_LENGTH_BYTES__), nullable=False)
                 )

keyword_index = Table('KeywordIndex', metadata,
                      Column('ID', Integer(), primary_key=True, autoincrement=True),
                      Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                      Column('Keyword', ForeignKey('Keyword.ID'), nullable=False),
                      )

key_value_index = Table('KeyValueIndex', metadata,
                        Column('ID', Integer(), primary_key=True, autoincrement=True),
                        Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                        Column('Keyword', ForeignKey('Keyword.ID'), nullable=False),
                        Column('Value', String(64)),
                        Column('IsNumeric', Boolean(), default=False),
                        )


class ContextDB:
    def __init__(self, metadata=metadata, path=conf.__CONTEXERE_CACHE_DB__):
        self.metadata = metadata
        self.path = path
        self.engine = create_engine('sqlite://' + str(self.path))
        self.inspector = inspect(self.engine)
        self.connection = None
        self.updated = {table: {} for table in self.metadata.tables}

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return True

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def connect(self):
        self.connection = self.engine.connect()
        return self.connection

    def read(self, stmt):
        with self.engine.begin() as conn:
            df = pd.read_sql_query(stmt, conn)
        return df

    def select_all(self, table):
        with self.engine.begin() as conn:
            df = pd.read_sql_query(select(self.metadata.tables[table]), conn)
        return df

    def get_researchers(self):
        return self.select_all('Researcher')

    def exists(self, table_name, data):
        """
        Test if table `table_name` already has a record having the
        """
        assert set(data.keys()).issubset(set(self.metadata.tables[table_name].columns.keys()))
        unique_cols = [col for col in self.metadata.tables[table_name].columns
                       if not col.nullable and (table_name == 'RAG' or col.name != 'ID')]
        predicates = [col == data[col.name] for col in unique_cols]
        print(table_name, 'predicates', predicates)
        stmt = select(self.metadata.tables[table_name].columns.ID).where(and_(*predicates))
        with self.engine.begin() as conn:
            existing_ID = conn.execute(stmt).scalar()
        return existing_ID

    def upsert(self, table_name, data):
        assert set(data.keys()).issubset(set(self.metadata.tables[table_name].columns.keys()))
        record_id = self.exists(table_name, data)
        if record_id is None:
            record_id = self.insert(table_name, data)
        return record_id



    def insert(self, table_name, data):
        """
        Inserts data given as dictionary inside a transaction and returns the new ID.
        """
        print('Insert', table_name)
        print(data)
        # minimal validation
        table = self.metadata.tables[table_name]
        for colname, col in table.columns.items():
            if (not col.nullable) and (not col.type.python_type == int) and colname not in data:
                raise ValueError(f"{table_name}.{colname} is required")

        stmt = (
            insert(table)
            .values(**data)
            .returning(table.c.ID)
        )

        with self.engine.begin() as conn:
            try:
                result = conn.execute(stmt)
                new_id = result.scalar_one()
                return new_id
            except IntegrityError:
                # Name is unique; duplicates will raise here
                # Transaction auto-rolls back due to context manager
                raise

if __name__ == '__main__':
    db = ContextDB(path='')
    db.create_tables()
    print(db.inspector.get_table_names())
