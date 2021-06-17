

- Introdução a sistemas distribuídos: objetivos, caracterização, classificação e desafios. 

- Comunicação em Sistemas Distribuídos: arquitetura em camadas, RMC, comunicação por troca de mensagens, disseminação de dados.
  - Encoding (JSON, Protobuf)
  - RPC (gRPC)
  - Messaging (Kafka)
  
- Gerenciamento de recursos: threads, processos, virtualização, escalabilidade, balanceamento de carga. 
  - Kernel Linux + Docker
  - Google Maglev
  - Envoy thread model
  - Kafka partition thread model + consumer group (processos)
  - KVM (?)
  
- Coordenação, Sincronização de processos, relógio físico e lógico, exclusão mútua, eleição, 
  - etcd + raft
  - Google Spanner (relógios) vs CockroachDB
  
- Tolerância a falhas, replicação e consistência 
  - PostgreSQL (ACID, 2PC, MVCC)
  - Jepsen
  - DynamoDB
  - Como a internet funciona

- Modelos de Sistemas Distribuídos: baseados em objetos, serviços. Computação em nuvem. 
Middleware e ferramentas para sistemas distribuídos, ferramentas para computação distribuída
  - 
