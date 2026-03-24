# Guia de Desenvolvimento

## Setup Inicial

### 1. Instalar Dependências

```bash
npm install
```

### 2. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

### 3. Iniciar Ambiente Docker

```bash
npm run dev
```

## Estrutura de um Microserviço

Cada microserviço segue a seguinte estrutura:

```
services/service-name/
├── src/
│   ├── index.ts              # Ponto de entrada
│   ├── config/               # Configurações
│   ├── controllers/          # Controladores HTTP
│   ├── services/             # Lógica de negócio
│   ├── repositories/         # Acesso a dados
│   ├── models/               # Modelos de dados
│   ├── middleware/           # Middlewares
│   ├── utils/                # Utilitários
│   └── types/                # Tipos TypeScript
├── __tests__/                # Testes
├── Dockerfile
├── package.json
└── tsconfig.json
```

## Padrões de Código

### TypeScript

- Use tipos explícitos sempre que possível
- Evite `any`
- Use interfaces para contratos públicos
- Use tipos para dados internos

### Estrutura de Serviço

```typescript
// services/my-service/src/index.ts
import express from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.MY_SERVICE_PORT || 3001;

// Middleware
app.use(express.json());

// Routes
app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// Start
app.listen(port, () => {
  console.log(`Service listening on port ${port}`);
});
```

### Repositório (Data Access)

```typescript
// services/my-service/src/repositories/user.repository.ts
import { Pool } from 'pg';

export class UserRepository {
  constructor(private pool: Pool) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async create(user: CreateUserInput): Promise<User> {
    const result = await this.pool.query(
      'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *',
      [user.email, user.name]
    );
    return result.rows[0];
  }
}
```

### Serviço (Business Logic)

```typescript
// services/my-service/src/services/user.service.ts
import { UserRepository } from '../repositories/user.repository';

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUserById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async createUser(input: CreateUserInput): Promise<User> {
    // Validação
    if (!input.email || !input.name) {
      throw new Error('Email and name are required');
    }

    // Lógica de negócio
    return this.userRepository.create(input);
  }
}
```

### Controlador (HTTP Handler)

```typescript
// services/my-service/src/controllers/user.controller.ts
import { Request, Response } from 'express';
import { UserService } from '../services/user.service';

export class UserController {
  constructor(private userService: UserService) {}

  async getUser(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.getUserById(req.params.id);
      res.json(user);
    } catch (error) {
      res.status(404).json({ error: 'User not found' });
    }
  }

  async createUser(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.createUser(req.body);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }
}
```

## Testes

### Executar Testes

```bash
npm test
npm test:watch
npm test:coverage
```

### Estrutura de Teste

```typescript
// services/my-service/__tests__/services/user.service.test.ts
import { UserService } from '../../src/services/user.service';
import { UserRepository } from '../../src/repositories/user.repository';

describe('UserService', () => {
  let userService: UserService;
  let userRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    userRepository = {
      findById: jest.fn(),
      create: jest.fn(),
    } as any;

    userService = new UserService(userRepository);
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const user = { id: '1', email: 'test@example.com', name: 'Test' };
      userRepository.findById.mockResolvedValue(user);

      const result = await userService.getUserById('1');

      expect(result).toEqual(user);
      expect(userRepository.findById).toHaveBeenCalledWith('1');
    });

    it('should throw error when user not found', async () => {
      userRepository.findById.mockResolvedValue(null);

      await expect(userService.getUserById('1')).rejects.toThrow('User not found');
    });
  });
});
```

## Comunicação Entre Serviços

### Via Message Broker (Assíncrono)

```typescript
// Publicar evento
import amqp from 'amqplib';

const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();

await channel.assertExchange('orders', 'topic', { durable: true });
await channel.publish(
  'orders',
  'order.created',
  Buffer.from(JSON.stringify({ orderId: '123', status: 'created' }))
);
```

```typescript
// Consumir evento
const queue = await channel.assertQueue('order-service-queue', { durable: true });
await channel.bindQueue(queue.queue, 'orders', 'order.*');

channel.consume(queue.queue, (msg) => {
  if (msg) {
    const event = JSON.parse(msg.content.toString());
    console.log('Received event:', event);
    channel.ack(msg);
  }
});
```

### Via HTTP (Síncrono)

```typescript
// Chamar outro serviço
import axios from 'axios';

const response = await axios.get('http://material-service:3003/api/v1/materials/123');
const material = response.data;
```

## Banco de Dados

### Criar Tabela

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Executar Query

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## Cache com Redis

```typescript
import redis from 'redis';

const client = redis.createClient({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
});

// Set
await client.set('user:123', JSON.stringify(user), 'EX', 3600);

// Get
const cached = await client.get('user:123');
```

## Logging

```typescript
// Usar console para desenvolvimento
console.log('Info message');
console.warn('Warning message');
console.error('Error message');

// Em produção, integrar com Elasticsearch/Kibana
```

## Linting e Formatação

```bash
# Lint
npm run lint

# Formatar
npm run format
```

## Deployment

### Build

```bash
npm run build
```

### Docker

```bash
docker build -t erp-service:1.0.0 .
docker run -p 3001:3001 erp-service:1.0.0
```

## Troubleshooting

### Erro de conexão com banco de dados

Verifique:
1. PostgreSQL está rodando: `docker ps | grep postgres`
2. Credenciais em `.env`
3. Rede Docker: `docker network ls`

### Erro de conexão com Redis

Verifique:
1. Redis está rodando: `docker ps | grep redis`
2. Porta correta em `.env`
3. Senha em `.env`

### Erro de conexão com RabbitMQ

Verifique:
1. RabbitMQ está rodando: `docker ps | grep rabbitmq`
2. Credenciais em `.env`
3. VHOST em `.env`

## Recursos Úteis

- [Express.js Documentation](https://expressjs.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Redis Documentation](https://redis.io/documentation)
