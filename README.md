# Projeto-POO-F1

# DESCRIÇÃO

Sistema de Gerenciamento de Campeonato de Fórmula 1, que engloba:

    A estrutura do campeonato (temporada, corridas, resultados, pontuação)

    A gestão interna das equipes (pilotos, engenheiros, mecânicos, carros, testes)

# CLASSES
1. classes abstratas
 
    Pessoa ()

    Funcionario (herda de Pessoa) – base para Piloto, Engenheiro, Mecânico
    
2. Pessoas / Funcionários

    Piloto (herda de Funcionario)

    Engenheiro (herda de Funcionario)

    Mecanico (herda de Funcionario)

    ChefeEquipe (herda de Funcionario)

4. Equipe e Recursos

    Equipe

    Carro

    Departamento

    TesteDePista

5. Campeonato / Corridas

    Temporada

    Corrida

    ResultadoCorrida (tabela associativa entre Corrida, Piloto e Equipe, com posição e pontos)
