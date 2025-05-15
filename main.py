from abc import ABC, abstractmethod

class Pessoa:
    def __init__(self, nome, email):
        self.nome = nome
        self._email = email

    def info(self):
        print(f'nome: {self.nome}, email: {self.email}')

class Funcionario(Pessoa):
    def __init__(self, nome, email, cpf, data_contratacao, salario, id_departamento, id_equipe):
        super().__init__(nome, email):
        self.cpf = cpf
        self.data_contratacao = data_contratacao
        self.salario = salario
        self.id_departamento = id_departamento
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
    
    