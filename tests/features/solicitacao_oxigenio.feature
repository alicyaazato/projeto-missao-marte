# language: pt
Funcionalidade: Solicitacao de suprimentos de oxigenio
  Como astronauta do habitat de Marte
  Quero solicitar cota extra de oxigenio
  Para manter a vida a bordo dentro das regras de racionamento

  Cenario: Solicitacao em condicoes normais
    Dado um habitat com 1000 kg de oxigenio e 4 astronautas
    Quando o astronauta "Ana" solicita 50 kg de oxigenio
    Entao a solicitacao e aprovada
    E o estoque de oxigenio passa a ser 950 kg
    E nenhum alerta e enviado para a Terra

  Cenario: Solicitacao em crise dispara alerta
    Dado um habitat com 21.8 kg de oxigenio e 4 astronautas
    Quando o astronauta "Joao" solicita 5 kg de oxigenio
    Entao a solicitacao e aprovada
    E um alerta "CRITICO" e enviado para a Terra

  Cenario: Solicitacao acima da cota de racionamento
    Dado um habitat com 1000 kg de oxigenio e 4 astronautas
    Quando o astronauta "Maria" solicita 500 kg de oxigenio
    Entao a solicitacao e negada por exceder a cota
    E o estoque de oxigenio passa a ser 1000 kg
