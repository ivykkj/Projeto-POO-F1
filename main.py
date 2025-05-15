from abc import ABC, abstractmethod

class Pessoa:
    def __init__(self, nome, email, cpf, ):
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def info(self):
        print(f'nome: {self.nome}, email: {self.email}, cpf: {self.cpf}')

class Funcionario(Pessoa):
    def __init__(self, nome, email, cpf, data_contratacao, salario, id_equipe):
        super().__init__(nome, email, cpf)
        self.data_contratacao = data_contratacao
        self.salario = salario
        self.id_equipé = id_equipe

    @property
    def salario(self):
        return self.__salario
    
    @salario.setter
    def salario(self, salario):
        if salario > 0:
            self.__salario = salario
        else:
            print('Salário Inválido')

    @property
    def salario_anual(self):
        return self.__salario * 12
    
class Piloto(Funcionario):
    def __init__(self, data_contratacao, salario, id_equipe, numero_carro, nacionalidade):
        super().__init__(data_contratacao, salario, id_equipe)
        self.numero_carro = numero_carro
        self.nacionalidade = nacionalidade

class Engenheiro(Funcionario):
    def __init__(self, data_contratacao, salario, id_equipe, especialidade, nivel_experiencia):
        super().__init__(data_contratacao, salario, id_equipe)
        self.especialidade = especialidade
        self.nivel_experiencia = nivel_experiencia

class ChefeEquipe(Funcionario):
    def __init__(self, data_contratacao, salario, id_equipe, anos_experiencia):
        super().__init__(data_contratacao, salario, id_equipe)
        self.anos_experiencia = anos_experiencia

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

