import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData, Table
from sqlalchemy import create_engine, insert, select

from contexere import conf

rag_id_length = conf.__MAX_PROJECT_ID_LENGTH__ + 5  # year 2, month 1, day 1, enumerator 1
metadata = MetaData()

projects = Table('Project', metadata,
                 Column('Name', String(conf.__MAX_PROJECT_ID_LENGTH__), primary_key=True, unique=True),
                 Column('Description', String(255)),
                 )

projects = Table('Researcher', metadata,
                 Column('ID', Integer(), primary_key=True, unique=True),
                 Column('Name', String(conf.__MAX_RESEARCHER_NAME_LENGTH__), unique=True, nullable=False),
                 Column('Email', String(255)),
                 )

research_artefact_groups = Table('RAGroup', metadata,
                                 Column('ID', String(rag_id_length), primary_key=True, unique=True,
                                        index=True, nullable=False),
                                 Column('Project', ForeignKey('Project.Name'), nullable=False),
                                 Column('Date', String(4), nullable=False),
                                 Column('Enumerator', String(1), nullable=False),
                                 Column('ResearcherID', ForeignKey('Researcher.ID'), nullable=False),
                                 )

research_knowledge_graph = Table('KnowledgeGraph', metadata,
                                 Column('Parent', ForeignKey('RAG.ID'), nullable=False),
                                 Column('Child', ForeignKey('RAG.ID'), nullable=False),
                                 )

research_artefact_paths = Table('Paths', metadata,
                                Column('ID', Integer(), primary_key=True, nullable=False),
                                Column('Path', String(conf.__MAX_PATH_LENGTH_BYTES__), nullable=False),
                                )

research_artefacts = Table('RArtefact', metadata,
                           Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                           Column('FileName', String(conf.__MAX_FILENAME_LENGTH_BYTES__), nullable=False),
                           Column('FileExtension', String(conf.__MAX_FILE_EXTENSION_LENGTH_BYTES__), nullable=False),
                           Column('Path', ForeignKey('research_artefacts_path.ID'), nullable=False),
                           Column('IsGenerator', Boolean(), default=False),
                           )

research_notes = Table('ResearchNote', metadata,
                       Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                       Column('FileName', String(conf.__MAX_FILENAME_LENGTH_BYTES__), nullable=False),
                       Column('FileExtension', String(conf.__MAX_FILE_EXTENSION_LENGTH_BYTES__), nullable=False),
                       Column('Path', ForeignKey('research_artefacts_path.ID'), nullable=False),
                       Column('Quote', String(conf.__MAX_QUOTE_LENGTH__)),
                       Column('LineNr', Integer(), nullable=False),
                       )

keywords = Table('Keyword', metadata,
                 Column('ID', Integer(), primary_key=True, nullable=False),
                 Column('Keyword', String(conf.__MAX_KEYWORD_LENGTH_BYTES__), nullable=False)
                 )

keyword_index = Table('KeywordIndex', metadata,
                      Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                      Column('Keyword', ForeignKey('Keyword.ID'), nullable=False),
                      )

key_value_index = Table('KeyValueIndex', metadata,
                        Column('RAG', ForeignKey('RAG.ID'), nullable=False),
                        Column('Keyword', ForeignKey('Keyword.ID'), nullable=False),
                        Column('Value', String(64)),
                        Column('IsNumeric', Boolean(), default=False),
                        )


class ContextDB:
    def __init__(self, db_file_path=conf.__CONTEXERE_CACHE_DB__):
        self.engine = create_engine('sqlite:////' + str(db_file_path))
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return True

    def connect(self):
        self.connection = self.engine.connect()
        return self.connection
