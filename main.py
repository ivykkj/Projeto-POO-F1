from bd_config import Base, engine
from sqlalchemy import Piloto, Corrida, Temporada, ResultadoCorrida

Base.metadata.create_all(engine)