# Setup Guide - ERP para Gráficas Expressas

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Docker**: 20.10 ou superior
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  
- **Docker Compose**: 2.0 ou superior
  - Geralmente incluído com Docker Desktop
  - Verifique: `docker-compose --version`

- **Git**: 2.30 ou superior
  - [Download Git](https://git-scm.com/downloads)

- **Node.js**: 18 ou superior (opcional, para desenvolvimento local)
  - [Download Node.js](https://nodejs.org/)

## Instalação Rápida

### 1. Clone o Repositório

```bash
git clone <repository-url>
cd erp-grafica-expressa
```

### 2. Configure o Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite conforme necessário (opcional para desenvolvimento)
# nano .env  ou  code .env
```

### 3. Inicie os Containers

```bash
# Opção 1: Usando npm
npm run dev

# Opção 2: Usando docker-compose diretamente
docker-compose up -d

# Opção 3: Usando make (se disponível)
make dev
```

### 4. Verifique o Status

```bash
# Verifique se todos os containers estão rodando
docker-compose ps

# Teste a API Gateway
curl http://localhost:3000/health
```

## Verificação de Saúde

Após iniciar, verifique se todos os serviços estão saudáveis:

### API Gateway
```bash
curl http://localhost:3000/health
# Resposta esperada: {"status":"ok","timestamp":"..."}
```

### PostgreSQL
```bash
docker-compose exec postgres psql -U erp_user -d erp_grafica -c "SELECT 1"
# Resposta esperada: 1
```

### Redis
```bash
docker-compose exec redis redis-cli ping
# Resposta esperada: PONG
```

### RabbitMQ
```bash
# Acesse o Management UI em http://localhost:15672
# Usuário: guest
# Senha: guest
```

### Elasticsearch
```bash
curl -u elastic:elastic_password_dev http://localhost:9200/
# Resposta esperada: JSON com informações do cluster
```

### MinIO
```bash
# Acesse o Console em http://localhost:9001
# Usuário: minioadmin
# Senha: minioadmin_dev
```

## Parar o Ambiente

```bash
# Opção 1: Usando npm
npm run dev:down

# Opção 2: Usando docker-compose
docker-compose down

# Opção 3: Usando make
make dev-down
```

## Limpar Dados

Para remover todos os dados e começar do zero:

```bash
# Remove containers e volumes
docker-compose down -v

# Reinicia tudo
npm run dev
```

## Troubleshooting

### Erro: "Port already in use"

Se uma porta já está em uso, você pode:

1. **Mudar a porta em `.env`**:
   ```bash
   API_GATEWAY_PORT=3001  # Mude de 3000 para 3001
   ```

2. **Ou liberar a porta**:
   ```bash
   # Linux/Mac
   lsof -i :3000
   kill -9 <PID>

   # Windows
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   ```

### Erro: "Cannot connect to Docker daemon"

Certifique-se de que:
1. Docker Desktop está rodando
2. Você tem permissão para usar Docker
3. No Linux, adicione seu usuário ao grupo docker:
   ```bash
   sudo usermod -aG docker $USER
   ```

### Erro: "Database connection refused"

Verifique:
1. PostgreSQL está rodando: `docker-compose ps postgres`
2. Credenciais em `.env` estão corretas
3. Aguarde alguns segundos para o banco inicializar

### Erro: "Cannot find module"

Se receber erro de módulos faltando:

```bash
# Limpe e reinstale
npm run clean
npm install
npm run dev
```

### Logs não aparecem

```bash
# Ver logs de todos os containers
npm run dev:logs

# Ver logs de um serviço específico
docker-compose logs -f postgres

# Ver últimas 100 linhas
docker-compose logs --tail=100
```

## Desenvolvimento Local

### Instalar Dependências

```bash
npm install
```

### Executar Testes

```bash
npm test
npm test:watch
npm test:coverage
```

### Lint e Formatação

```bash
npm run lint
npm run format
```

## Variáveis de Ambiente Importantes

### Segurança (Alterar em Produção)

```env
JWT_SECRET=your_jwt_secret_key_change_in_production
DB_PASSWORD=erp_password_dev
REDIS_PASSWORD=redis_password_dev
ELASTICSEARCH_PASSWORD=elastic_password_dev
MINIO_ROOT_PASSWORD=minioadmin_dev
```

### Banco de Dados

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=erp_grafica
DB_USER=erp_user
DB_PASSWORD=erp_password_dev
```

### Cache

```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_password_dev
```

### Message Broker

```env
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### Armazenamento

```env
MINIO_HOST=minio
MINIO_PORT=9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin_dev
```

## Próximos Passos

1. **Leia a documentação**:
   - [README.md](./README.md) - Visão geral do projeto
   - [DEVELOPMENT.md](./DEVELOPMENT.md) - Guia de desenvolvimento

2. **Explore os serviços**:
   - Acesse http://localhost:3000/health
   - Verifique RabbitMQ em http://localhost:15672
   - Verifique MinIO em http://localhost:9001

3. **Comece a desenvolver**:
   - Crie um novo serviço em `services/`
   - Implemente a lógica de negócio
   - Escreva testes
   - Faça commit e push

## Recursos Úteis

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Redis Documentation](https://redis.io/documentation)
- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)

## Suporte

Se encontrar problemas:

1. Verifique os logs: `npm run dev:logs`
2. Consulte o [Troubleshooting](#troubleshooting)
3. Abra uma issue no repositório
4. Entre em contato com a equipe de desenvolvimento
