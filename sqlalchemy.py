from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.declarative import declared_attr
from bd_config import Base
from abc import ABC, abstractmethod

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String)
    cpf = Column(String, unique=True)
    data_contratacao = Column(String)
    salario = Column(Float)
    equipe_id = Column(Integer, ForeignKey('equipes.id'))
    tipo = Column(String)  

    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': tipo
    }

    @validates('salario')
    def validar_salario(self, key, salario):
        if salario <= 0:
            raise ValueError("Salário inválido")
        return salario
    
    @property
    def salario_anual(self):
        return self.salario * 12 if self.salario else 0
    
    @classmethod
    def total_funcionarios(cls, session):
        return session.query(cls).count()
    
    @abstractmethod
    def info(self):
        pass

    equipe = relationship("Equipe", back_populates="funcionarios")

class Piloto(Funcionario):
    __tablename__ = 'pilotos'
    id = Column(Integer, ForeignKey('funcionarios.id'), primary_key=True)

    numero_carro = Column(Integer)
    nacionalidade = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'piloto',
    }

    def contar_poles_query(self, session):
        return session.query(Qualificacao).filter(Qualificacao.piloto_id == self.id, Qualificacao.q1 != None).count()


    def info(self):
        return f'Piloto: {self.nome}, Carro #{self.numero_carro}, Nacionalidade: {self.nacionalidade}, Equipe: {self.equipe.nome if self.equipe else "Sem equipe"}'

class Engenheiro(Funcionario):
    __tablename__ = 'engenheiros'
    id = Column(Integer, ForeignKey('funcionarios.id'), primary_key=True)

    especialidade = Column(String)
    nivel_experiencia = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'engenheiro',
    }

    def promover(self):
        if self.nivel_experiencia is not None and self.nivel_experiencia < 10:
            self.nivel_experiencia += 1
            return f"{self.nome} promovido para nível {self.nivel_experiencia}"
        return f"{self.nome} já está no nível máximo ou sem nível definido"
    
    def info(self):
        return f'Engenheiro: {self.nome}, Especialidade: {self.especialidade}, Nível de Experiência: {self.nivel_experiencia}, Equipe: {self.equipe.nome if self.equipe else "Sem equipe"}'

class ChefeEquipe(Funcionario):
    __tablename__ = 'chefes_equipes'
    id = Column(Integer, ForeignKey('funcionarios.id'), primary_key=True)

    anos_experiencia = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'chefe',
    }

    def info(self):
        return f'Chefe de Equipe: {self.nome}, Experiência: {self.anos_experiencia} anos, Equipe: {self.equipe.nome if self.equipe else "Sem equipe"}'

class Equipe(Base):
    __tablename__ = 'equipes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    pais = Column(String, nullable=False)

    funcionarios = relationship("Funcionario", back_populates="equipe")
    carros = relationship("Carro", back_populates="equipe")

    def total_funcionarios(self):
        return len(self.funcionarios)

    def listar_pilotos(self):
        return [f for f in self.funcionarios if isinstance(f, Piloto)]

class Carro(Base):
    __tablename__ = 'carros'
    id = Column(Integer, primary_key=True)
    modelo = Column(String)
    motor = Column(String)
    ano = Column(Integer)
    equipe_id = Column(Integer, ForeignKey('equipes.id'))

    equipe = relationship("Equipe", back_populates="carros")

class Temporada(Base):
    __tablename__ = 'temporadas'
    id = Column(Integer, primary_key=True)
    ano = Column(Integer, nullable=False)

    corridas = relationship("Corrida", back_populates="temporada", cascade="all, delete-orphan")

    def definir_campeao(self, session):
        temporada_completa = session.query(Temporada).options(
            joinedload(Temporada.corridas).joinedload(Corrida.resultados).joinedload(ResultadoCorrida.piloto)
        ).filter_by(id=self.id).first()

        pontos_por_piloto = {}

        for corrida in temporada_completa.corridas:
            for resultado in corrida.resultados:
                piloto = resultado.piloto
                pontos_por_piloto[piloto] = pontos_por_piloto.get(piloto, 0) + resultado.pontos

        campeao = None
        maior_pontuacao = -1

        for piloto, pontos in pontos_por_piloto.items():
            if pontos > maior_pontuacao:
                maior_pontuacao = pontos
                campeao = piloto

        return campeao, maior_pontuacao

class Corrida(Base):
    __tablename__ = 'corridas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data = Column(Date)
    pais = Column(String)
    clima = Column(String)
    temporada_id = Column(Integer, ForeignKey('temporadas.id'))

    @staticmethod
    def calcular_pontuacao(posicao):
        pontos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        if 1 <= posicao <= 10:
            return pontos[posicao - 1]
        return 0
    
    def __repr__(self):
        return f"<Corrida(nome={self.nome}, data={self.data}, pais={self.pais})>"

    temporada = relationship("Temporada", back_populates="corridas")
    resultados = relationship("ResultadoCorrida", back_populates="corrida")

class ResultadoCorrida(Base):
    __tablename__ = 'resultados_corrida'
    id = Column(Integer, primary_key=True)
    piloto_id = Column(Integer, ForeignKey('funcionarios.id'))
    corrida_id = Column(Integer, ForeignKey('corridas.id'))
    equipe_id = Column(Integer, ForeignKey('equipes.id'))
    posicao = Column(Integer)
    pontos = Column(Integer)

    piloto = relationship("Piloto")
    corrida = relationship("Corrida", back_populates="resultados")
    equipe = relationship("Equipe")

    def __init__(self, piloto=None, corrida=None, equipe=None, posicao=None, pontos=None):
        self.piloto = piloto
        self.corrida = corrida
        self.equipe = equipe
        self.posicao = posicao
        self.pontos = pontos if pontos is not None else Corrida.calcular_pontuacao(posicao)

    @validates('posicao')
    def validar_posicao(self, key, posicao):
        if posicao is None or posicao < 1 or posicao > 20:
            raise ValueError("Posição inválida, deve ser entre 1 e 20")
        return posicao

    def __repr__(self):
        return f"<ResultadoCorrida(piloto={self.piloto.nome if self.piloto else None}, corrida={self.corrida.nome if self.corrida else None}, posicao={self.posicao}, pontos={self.pontos})>"

class TreinoLivre(Base):
    __tablename__ = 'treinos_livres'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    melhor_volta = Column(Float)
    sessao = Column(String)

    piloto_id = Column(Integer, ForeignKey('funcionarios.id'))
    carro_id = Column(Integer, ForeignKey('carros.id'))
    corrida_id = Column(Integer, ForeignKey('corridas.id'))

    piloto = relationship("Piloto")
    carro = relationship("Carro")
    corrida = relationship("Corrida")

    @classmethod
    def melhor_treino(cls, treinos):
        if not treinos:
            return None

        melhor = treinos[0]
        for treino in treinos[1:]:
            if treino.melhor_volta < melhor.melhor_volta:
                melhor = treino
        return melhor

class Qualificacao(Base):
    __tablename__ = 'qualificacoes'
    id = Column(Integer, primary_key=True)
    corrida_id = Column(Integer, ForeignKey('corridas.id'))
    piloto_id = Column(Integer, ForeignKey('funcionarios.id'))

    corrida = relationship("Corrida")
    piloto = relationship("Piloto")

    def adicionar_tempo(self, fase, piloto, tempo):
        novo_tempo = TempoQualificacao(
            fase=fase,
            piloto_id=piloto.id,
            tempo=tempo,
            qualificacao=self
        )
        self.tempos.append(novo_tempo)

    def obter_grid_largada(self):
        q3_tempos = [t for t in self.tempos if t.fase == 'Q3']

        q3_tempos.sort(key=lambda t: t.tempo)

        return [t.piloto for t in q3_tempos]

    def obter_pole_position(self):
        grid = self.obter_grid_largada()
        return grid[0] if grid else None

    tempos = relationship("TempoQualificacao", back_populates="qualificacao", cascade="all, delete-orphan")

class TempoQualificacao(Base):
    __tablename__ = 'tempos_qualificacao'
    id = Column(Integer, primary_key=True)
    qualificacao_id = Column(Integer, ForeignKey('qualificacoes.id'))
    fase = Column(String)  
    piloto_id = Column(Integer, ForeignKey('funcionarios.id'))
    tempo = Column(Float)

    qualificacao = relationship("Qualificacao", back_populates="tempos")
    piloto = relationship("Piloto")
