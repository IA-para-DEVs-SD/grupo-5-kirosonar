# ERP para Gráficas Expressas

Sistema ERP integrado para gerenciar operações de gráficas expressas, desde recepção de pedidos até entrega final.

## Visão Geral

Este é um sistema de microserviços modular projetado para:
- Gerenciar pedidos e orçamentos de impressão
- Controlar produção e fluxo de trabalho
- Gerenciar materiais e estoque
- Agendar recursos e máquinas
- Controlar qualidade
- Gerenciar financeiro e faturamento
- Rastrear entregas
- Gerar relatórios e análises

## Arquitetura

```
Frontend (Web/Mobile)
    ↓
API Gateway (Roteamento, Autenticação)
    ↓
Microserviços (11 serviços independentes)
    ↓
Message Broker (RabbitMQ/Kafka)
    ↓
Banco de Dados (PostgreSQL, Redis, Elasticsearch, MinIO)
```

## Microserviços

- **Order Service**: Gestão de pedidos e orçamentos
- **Production Service**: Ordens de produção e fluxo
- **Material Service**: Insumos e estoque
- **Resource Service**: Máquinas e agendamento
- **Quality Service**: Controle de qualidade
- **Financial Service**: Faturamento e pagamentos
- **Customer Service**: Clientes e CRM
- **Delivery Service**: Rastreamento e entrega
- **HR Service**: Funcionários e turnos
- **Notification Service**: Alertas e notificações
- **Reporting Service**: Relatórios e dashboards

## Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (para desenvolvimento local)
- npm 9+

## Configuração Inicial

### 1. Clone o repositório

```bash
git clone <repository-url>
cd erp-grafica-expressa
```

### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário para seu ambiente.

### 3. Inicie os containers

```bash
npm run dev
```

Isso iniciará todos os serviços:
- PostgreSQL (porta 5432)
- Redis (porta 6379)
- RabbitMQ (porta 5672, Management UI: 15672)
- Elasticsearch (porta 9200)
- MinIO (porta 9000, Console: 9001)
- API Gateway (porta 3000)

### 4. Verifique a saúde dos serviços

```bash
curl http://localhost:3000/health
```

## Desenvolvimento

### Estrutura de Diretórios

```
.
├── services/              # Microserviços
│   ├── api-gateway/
│   ├── order-service/
│   ├── production-service/
│   └── ...
├── scripts/               # Scripts de utilidade
├── docker-compose.yml     # Configuração Docker
├── .env.example          # Variáveis de ambiente
└── README.md
```

### Comandos Úteis

```bash
# Iniciar ambiente de desenvolvimento
npm run dev

# Parar containers
npm run dev:down

# Ver logs
npm run dev:logs

# Reconstruir containers
npm run dev:rebuild

# Executar testes
npm test

# Executar linter
npm run lint

# Formatar código
npm run format
```

## Banco de Dados

### Conexão

```
Host: localhost
Port: 5432
Database: erp_grafica
User: erp_user
Password: erp_password_dev (alterar em produção)
```

### Migrations

As migrations são executadas automaticamente ao iniciar o container PostgreSQL.

## Message Broker

### RabbitMQ Management UI

Acesse em: http://localhost:15672
- Usuário: guest
- Senha: guest

## Armazenamento de Arquivos

### MinIO Console

Acesse em: http://localhost:9001
- Usuário: minioadmin
- Senha: minioadmin_dev

Buckets:
- `arts`: Arquivos de arte (PDFs, imagens)
- `documents`: Documentos (notas fiscais, etc.)

## Elasticsearch

### Acesso

```
URL: http://localhost:9200
Usuário: elastic
Senha: elastic_password_dev
```

## Segurança

### Variáveis Críticas

As seguintes variáveis devem ser alteradas em produção:
- `JWT_SECRET`: Chave secreta para JWT
- `DB_PASSWORD`: Senha do banco de dados
- `REDIS_PASSWORD`: Senha do Redis
- `ELASTICSEARCH_PASSWORD`: Senha do Elasticsearch
- `MINIO_ROOT_PASSWORD`: Senha do MinIO

### Autenticação

O sistema usa JWT para autenticação. Todos os endpoints (exceto `/health` e `/api/v1/version`) requerem um token válido no header `Authorization: Bearer <token>`.

## Backup e Recuperação

### Backup Automático

Backups são executados automaticamente conforme configurado em `BACKUP_SCHEDULE` (padrão: 02:00 diariamente).

### Retenção

Backups são retidos por `BACKUP_RETENTION_DAYS` dias (padrão: 30 dias).

## Monitoramento

### Logs

Todos os logs são centralizados no Elasticsearch e podem ser consultados através de ferramentas como Kibana.

### Health Checks

Cada serviço expõe um endpoint `/health` para verificação de saúde.

## Troubleshooting

### Containers não iniciam

```bash
# Verifique os logs
npm run dev:logs

# Reconstrua os containers
npm run dev:rebuild
```

### Erro de conexão com banco de dados

```bash
# Verifique se o PostgreSQL está rodando
docker ps | grep postgres

# Verifique as credenciais em .env
```

### Porta já em uso

Altere as portas em `docker-compose.yml` ou em `.env`.

## Documentação

- [Design Técnico](./docs/design.md)
- [Requisitos](./docs/requirements.md)
- [Plano de Implementação](./docs/tasks.md)

## Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## Licença

Proprietary - Gráficas Expressas

## Suporte

Para suporte, entre em contato com a equipe de desenvolvimento.
