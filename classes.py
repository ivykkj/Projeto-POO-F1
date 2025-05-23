from abc import ABC, abstractmethod

class Funcionario(ABC):
    contador_funcionarios = 0

    def __init__(self, nome, email, cpf, data_contratacao, salario, equipe):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_contratacao = data_contratacao
        self.salario = salario
        self.equipe = equipe
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
    def __init__(self, nome, email, cpf, data_contratacao, salario, equipe, numero_carro, nacionalidade):
        super().__init__(nome, email, cpf, data_contratacao, salario, equipe)
        self.numero_carro = numero_carro
        self.nacionalidade = nacionalidade
        
    def contar_poles(self, qualificacao):
        return sum(1 for q in qualificacao if q.obter_pole_position() == self)

    def info(self):
        print(f'Piloto: {self.nome}, Carro #{self.numero_carro}, Nacionalidade: {self.nacionalidade}, Equipe: {self.equipe} ')

class Engenheiro(Funcionario):
    def __init__(self, nome, email, cpf, data_contratacao, salario, equipe, especialidade, nivel_experiencia):
        super().__init__(nome, email, cpf, data_contratacao, salario, equipe)
        self.especialidade = especialidade
        self.nivel_experiencia = nivel_experiencia

    def promover(self):
        if self.nivel_experiencia < 10:
            self.nivel_experiencia += 1
            print(f"{self.nome} promovido para nível {self.nivel_experiencia}")

    def info(self):
        print(f'Engenheiro: {self.nome}, Especialidade: {self.especialidade}, Nível: {self.nivel_experiencia}, Equipe: {self.equipe}')

class ChefeEquipe(Funcionario):
    def __init__(self, nome, email, cpf, data_contratacao, salario, equipe, anos_experiencia):
        super().__init__(nome, email, cpf, data_contratacao, salario, equipe)
        self.anos_experiencia = anos_experiencia

    def info(self):
        print(f'Chefe de Equipe: {self.nome}, Experiência: {self.anos_experiencia} anos, Equipe: {self.equipe}')

class Equipe:
    def __init__(self, nome, pais, chefe):
        self.nome = nome
        self.pais = pais
        self.chefe = chefe
        self.pilotos = []
        self.engenheiros = []

    def adicionar_piloto(self, piloto):
        self.pilotos.append(piloto)

    def adicionar_engenheiros(self, engenheiro):
        self.engenheiros.append(engenheiro)

class Carro:
    def __init__(self, modelo, motor, ano, equipe):
        self.modelo = modelo
        self.motor = motor
        self.ano = ano
        self.equipe = equipe

class TreinoLivre:
    def __init__(self, data, melhor_volta, sessao , piloto, carro, corrida):
        self.data = data
        self.melhor_volta = melhor_volta
        self.piloto = piloto
        self.carro = carro
        self.sessao = sessao  
        self.corrida = corrida

    @classmethod
    def melhor_treino(cls, treinos):
        if not treinos:
            return None

        melhor = treinos[0]
        for treino in treinos[1:]:
            if treino.melhor_volta < melhor.melhor_volta:
                melhor = treino
        return melhor

class Temporada:
    def __init__(self, ano):
        self.ano = ano
        self.corridas = []
        self.resultados = []
    
    def adicionar_corrida(self, corrida):
        self.corridas.append(corrida)

    def adicionar_resultado(self, resultado):
        self.resultados.append(resultado)

    def definir_campeao(self):
        pontos_por_piloto = {}

        for resultado in self.resultados:
            piloto = resultado.piloto
            pontos_por_piloto[piloto] = pontos_por_piloto.get(piloto, 0) + resultado.pontos

        campeao = None
        maior_pontuacao = -1

        for piloto in pontos_por_piloto:
            if pontos_por_piloto[piloto] > maior_pontuacao:
                maior_pontuacao = pontos_por_piloto[piloto]
                campeao = piloto

        return campeao, maior_pontuacao

class Qualificacao:
    def __init__(self, corrida, piloto, q1, q2, q3):
        self.corrida = corrida
        self.piloto = piloto
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

    def adicionar_tempo(self, fase, piloto, tempo):
        if fase == 'Q1':
            self.q1.append((piloto, tempo))
        elif fase == 'Q2':
            self.q2.append((piloto, tempo))
        elif fase == 'Q3':
            self.q3.append((piloto, tempo))

    def determinar_grid_largada(self):
        grid = []

        for i in range(len(self.q3)):
            menor = self.q3[0]
            for tempo in self.q3:
                if tempo[1] < menor[1]:
                    menor = tempo
            grid.append(menor)
            self.q3.remove(menor)
        return grid
    
    def obter_pole_position(self):
        grid = self.definir_grid_largada()
        return grid[0][0] 
    
class Corrida:
    pontos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    def __init__(self, nome, data, pais, clima, temporada):
        self.nome = nome
        self.data = data
        self.pais = pais
        self.temporada = temporada
        self.clima = clima
      
    def calcular_pontuacao(self, posicao):
        if 1 <= posicao <= 10:
            return Corrida.pontos[posicao - 1]
        return 0

class ResultadoCorrida:
    def __init__(self, piloto, corrida, equipe, posicao, pontos):
        self.piloto = piloto
        self.corrida = corrida
        self.equipe = equipe
        self.posicao = posicao
        self.pontos = pontos