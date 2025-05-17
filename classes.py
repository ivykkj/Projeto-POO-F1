from abc import ABC, abstractmethod

class Funcionario(ABC):
    contador_funcionarios = 0

    def __init__(self, nome, email, cpf, data_contratacao, salario, id_equipe):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_contratacao = data_contratacao
        self.salario = salario
        self.id_equipe = id_equipe
        Funcionario.contador_funcionarios += 1

    @property
    def salario(self):
        return self.__salario
    
    @salario.setter
    def salario(self, salario):
        if salario > 0:
            self.__salario = salario
        else:
            raise ValueError("salário inválido")
    
    @property
    def salario_anual(self):
        return self.__salario * 12

    @classmethod
    def total_funcionarios(cls):
        return cls.contador_funcionarios

    @abstractmethod
    def info(self):
        pass
    
class Piloto(Funcionario):
    def __init__(self, nome, email, cpf, data_contratacao, salario, id_equipe, numero_carro, nacionalidade):
        super().__init__(nome, email, cpf, data_contratacao, salario, id_equipe)
        self.numero_carro = numero_carro
        self.nacionalidade = nacionalidade

    def info(self):
        print(f'Piloto: {self.nome}, Carro #{self.numero_carro}, Nacionalidade: {self.nacionalidade}, Equipe: {self.id_equipe} ')

class Engenheiro(Funcionario):
    def __init__(self, nome, email, cpf, data_contratacao, salario, id_equipe, especialidade, nivel_experiencia):
        super().__init__(nome, email, cpf, data_contratacao, salario, id_equipe)
        self.especialidade = especialidade
        self.nivel_experiencia = nivel_experiencia

    def promover(self):
        if self.nivel_experiencia < 10:
            self.nivel_experiencia += 1
            print(f"{self.nome} promovido para nível {self.nivel_experiencia}")


    def info(self):
        print(f'Engenheiro: {self.nome}, Especialidade: {self.especialidade}, Nível: {self.nivel_experiencia}, Equipe: {self.id_equipe}')

class ChefeEquipe(Funcionario):
    def __init__(self, nome, email, cpf, data_contratacao, salario, id_equipe, anos_experiencia):
        super().__init__(nome, email, cpf, data_contratacao, salario, id_equipe)
        self.anos_experiencia = anos_experiencia

    def info(self):
        print(f'Chefe de Equipe: {self.nome}, Experiência: {self.anos_experiencia} anos, Equipe: {self.id_equipe}')

class Equipe:
    def __init__(self, nome, pais, chefe_id):
        self.nome = nome
        self.pais = pais
        self.chefe_id = chefe_id

class Carro:
    def __init__(self, modelo, motor, ano, equipe_id):
        self.modelo = modelo
        self.motor = motor
        self.ano = ano
        self.equipe_id = equipe_id

class TreinoLivre:
    def __init__(self, data, melhor_volta, piloto_id, carro_id):
        self.data = data
        self.melhor_volta = melhor_volta
        self.piloto_id = piloto_id
        self.carro_id = carro_id

class Temporada:
    def __init__(self, ano):
        self.ano = ano

class Qualificacao:
    def __init__(self, corrida_id, piloto_id, tempo_q1, tempo_q2, tempo_q3):
        self.corrida_id = corrida_id
        self.piloto_id = piloto_id
        self.tempo_q1 = tempo_q1
        self.tempo_q2 = tempo_q2
        self.tempo_q3 = tempo_q3

    
    

class Corrida:
    def __init__(self, nome, data, pais, clima, temporada_id, pontos):
        self.nome = nome
        self.data = data
        self.pais = pais
        self.temporada_id = temporada_id
        self.clima = clima
        self.pontos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


    def calcular_pontuacao(self, posicao):
        if 1 <= posicao <= 10:
            return self.pontos[posicao - 1]
        return 0

class ResultadoCorrida:
    def __init__(self, piloto_id, corrida_id, equipe_id, posicao, pontos):
        self.piloto_id = piloto_id
        self.corrida_id = corrida_id
        self.equipe_id = equipe_id
        self.posicao = posicao
        self.pontos = pontos 

