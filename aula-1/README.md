# Aula 1

Imagine que você acabou de entrar em um time de desenvolvimento de uma empresa de pagamentos digitais.

Você é responsável por manter um conjunto de sistemas que entregam a funcionalidade de registrar transações e depois consultar seu status. Utilize esse contexto para analisar os pontos a seguir.

Considere o diagrama da arquitetura dos componentes:

![Arquitetura](diagrams/arquitetura.png)

Considere os dois fluxos seguintes:

- Criar nova transação

![](diagrams/create_transaction.png)

- Listar transações

![](diagrams/list_transactions.png)

## Exercícios

1. Ainda é possível registrar transações quando uma das réplicas do `Cassandra` é desligada? E duas?

2. Quando o `Redis` está indisponível, ainda é possível consultar transações?

3. Caso o serviço `transactions` esteja fora do ar quando uma nova transação for publicada no kafka pelo `bff`, a transação será perdida? O que acontece quando `transactions` voltar ao ar?

4. Quais são as vantagens de transmitir os dados em Avro em vez de JSON do `bff` para o `Kafka`?

5. O `Kafka`, ao possibilitar o processamento assíncrono de transações pelo serviço `transactions`, permite com que o `bff` consiga responder com um __throughput__ maior, pois não é preciso esperar a latência do `Cassandra` e `antifraud`. Porém isso também traz suas desvantagens para a arquitetura. Liste duas desvantagens e justifique.

6. Analise o código do serviço de `transactions`. Quando o serviço `antifraud` estiver desligado, **ainda é possível registrar transações**? Qual vai ser o `status` final das transações nesse caso?

7. Quais são as **duas vantagens e desvantagens** de utilizar o envoy como __load balancer__ no contexto da interação entre os serviços `transactions` e `antifraud`?

8. O código enviar uma notificação de status por webhook para o `bff` está estruturado assim:

```python
def notify_status(transaction_id, status):
    try:
        resp = requests.patch(
            f"{BFF_HOST}/api/v1/transactions/{transaction_id}/status",
            json={"status": status},
        )

    except Exception as err:
        logging.error(f"failed to update status: {str(err)}")
        raise BFFStatusWebhookError(Exception)
```

a. Modifique esse código para que quando não for possível se comunicar com o serviço `bff`, continuar tentando enviar por mais 10 vezes antes de retornar um erro.

b. Ainda nesse contexto de interação entre os serviços `transactions` e `bff`, quais são as desvantagens de receber o status por __webhook__ para o `bff`?
