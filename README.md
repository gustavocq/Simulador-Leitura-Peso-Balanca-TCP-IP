# Simulador de Balança Rodoviária (TCP)

Este projeto é um simulador de balança rodoviária que envia valores de
peso via TCP, reproduzindo o comportamento real de um caminhão passando
pela balança. Código criado na intenção de facilitar testes em integrações 
de balanças nesse formato.

O ciclo simulado inclui:

1.  Subida gradual do peso (entrada do caminhão)
2.  Estabilização em 40.000
3.  Descida gradual do peso (saída do caminhão)
4.  Envio do valor especial 40001
5.  Envio de zeros por alguns segundos
6.  Reinício automático

## 🚀 Como executar

### Pré-requisitos

-   Python 3.10+

### Executando o servidor

``` bash
python simulador_balanca.py
```

O servidor será iniciado em:

    0.0.0.0:9000

## 🔌 Protocolo de comunicação

-   Protocolo: TCP
-   Porta padrão: 9000
-   Envio contínuo de leituras formatadas como:

```{=html}
<!-- -->
```
    )0  {PESO:05d}    00

Exemplos de mensagens:

    )0  01200    00
    )0  40000    00
    )0  40001    00
    )0  00000    00

## 🧪 Testando a conexão

### Telnet

``` bash
telnet 127.0.0.1 9000
```

### Netcat

``` bash
nc 127.0.0.1 9000
```

## 📄 Descrição do funcionamento

A lógica do simulador segue etapas:

-   Subida do peso com incrementos variáveis até 40.000
-   Manutenção de 40.000 por alguns segundos
-   Descida do peso até zero
-   Envio do valor especial 40001
-   Envio de zeros por 5 segundos
-   Recomeço automático do ciclo
