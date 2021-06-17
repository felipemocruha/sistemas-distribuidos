sequenceDiagram
	autonumber
	generator->>bff: register transaction
	bff->>kafka: transaction_created
	kafka->>transactions: transaction_created
	transactions->>envoy: validate transaction
	envoy->>antifraud: validate transaction (proxy)
	antifraud-->>transactions: status
	transactions->>cassandra: save transaction
	transactions->>bff: notify status (webhook)
	bff->>redis: update transaction


sequenceDiagram
	autonumber
	frontend->>bff: list transactions
	bff->>redis: list transaction
	bff-->>frontend: transactions
	
