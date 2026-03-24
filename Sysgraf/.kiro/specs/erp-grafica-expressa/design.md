# Design Técnico - ERP para Gráficas Expressas

## Overview

Este documento descreve a arquitetura técnica e design de um Sistema ERP integrado para gráficas expressas. O sistema foi projetado para gerenciar operações de alta velocidade com prazos curtos, oferecendo flexibilidade operacional e escalabilidade.

### Objetivos de Design

- Suportar operações de alta velocidade com prazos curtos
- Garantir rastreabilidade completa de pedidos
- Otimizar utilização de recursos e máquinas
- Manter integridade de dados e auditoria
- Escalar horizontalmente conforme demanda
- Integrar com sistemas externos (NF-e, fornecedores)

---

## Architecture

### Padrão Arquitetural: Microserviços Modular

Adotamos uma arquitetura de **microserviços modular** que combina os benefícios de modularidade com escalabilidade independente. Cada domínio de negócio é um serviço autônomo que se comunica através de APIs REST e eventos assíncronos.

### Componentes Principais

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  (Web Dashboard, Mobile App, Operador Interface)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API Gateway                                   │
│  (Roteamento, Autenticação, Rate Limiting, Logging)            │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  Microserviços                                   │
├─────────────────────────────────────────────────────────────────┤
│ • Order Service (Pedidos e Orçamentos)                          │
│ • Production Service (Ordens de Produção, Fluxo)               │
│ • Material Service (Insumos, Estoque)                          │
│ • Resource Service (Máquinas, Agendamento)                     │
│ • Quality Service (Controle de Qualidade)                      │
│ • Financial Service (Faturamento, Pagamentos)                  │
│ • Customer Service (Clientes, CRM)                             │
│ • Delivery Service (Rastreamento, Entrega)                     │
│ • HR Service (Funcionários, Turnos)                            │
│ • Notification Service (Alertas, Notificações)                 │
│ • Reporting Service (Relatórios, Dashboards)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              Message Broker & Event Bus                          │
│  (RabbitMQ/Kafka para comunicação assíncrona)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  Data Layer                                      │
├─────────────────────────────────────────────────────────────────┤
│ • PostgreSQL (Dados transacionais)                              │
│ • Redis (Cache, Sessões)                                        │
│ • Elasticsearch (Busca e Logs)                                  │
│ • S3/MinIO (Arquivos, Artes)                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

1. **Requisição do Cliente** → API Gateway
2. **Autenticação e Autorização** → Verificação de permissões
3. **Roteamento** → Microserviço apropriado
4. **Processamento** → Lógica de negócio
5. **Persistência** → Banco de dados
6. **Eventos** → Message Broker (para outros serviços)
7. **Resposta** → Cliente

---

## Components and Interfaces

### 1. API Gateway

**Responsabilidades:**
- Roteamento de requisições
- Autenticação e autorização
- Rate limiting e throttling
- Logging e monitoramento
- Transformação de requisições/respostas

**Endpoints Principais:**
```
POST   /api/v1/orders              - Criar pedido
GET    /api/v1/orders/:id          - Obter pedido
PUT    /api/v1/orders/:id          - Atualizar pedido
GET    /api/v1/orders              - Listar pedidos
POST   /api/v1/quotes              - Criar orçamento
GET    /api/v1/production/tasks    - Listar tarefas
POST   /api/v1/materials/reserve   - Reservar insumos
GET    /api/v1/resources/schedule  - Obter agenda
```

### 2. Order Service

**Responsabilidades:**
- Gerenciar pedidos e orçamentos
- Calcular preços automaticamente
- Converter orçamentos em pedidos
- Registrar alterações e histórico

**Interfaces:**
```
POST   /orders/create              - Criar novo pedido
POST   /orders/:id/convert-quote   - Converter orçamento
PUT    /orders/:id/update          - Atualizar pedido
GET    /orders/:id/history         - Histórico de alterações
POST   /quotes/calculate           - Calcular preço
```

### 3. Production Service

**Responsabilidades:**
- Gerenciar ordens de produção
- Controlar fluxo de produção
- Registrar progresso de tarefas
- Validar transições de estado

**Interfaces:**
```
POST   /production/orders/create   - Criar ordem de produção
PUT    /production/tasks/:id/start - Iniciar tarefa
PUT    /production/tasks/:id/complete - Completar tarefa
GET    /production/orders/:id      - Status da ordem
GET    /production/progress        - Progresso visual
```

### 4. Material Service

**Responsabilidades:**
- Gerenciar insumos e estoque
- Reservar materiais
- Atualizar consumo
- Gerar alertas de reposição

**Interfaces:**
```
POST   /materials/reserve          - Reservar insumos
PUT    /materials/:id/consume      - Registrar consumo
GET    /inventory/status           - Status do estoque
POST   /inventory/alerts           - Gerar alertas
```

### 5. Resource Service

**Responsabilidades:**
- Gerenciar máquinas e equipamentos
- Agendar recursos
- Verificar disponibilidade
- Reagendar automaticamente

**Interfaces:**
```
POST   /resources/schedule         - Agendar recurso
GET    /resources/availability     - Verificar disponibilidade
PUT    /resources/:id/unavailable  - Marcar indisponível
GET    /resources/calendar         - Calendário visual
```

### 6. Quality Service

**Responsabilidades:**
- Registrar inspeções de qualidade
- Criar ordens de retrabalho
- Manter histórico de defeitos
- Gerar relatórios de qualidade

**Interfaces:**
```
POST   /quality/inspect            - Registrar inspeção
POST   /quality/rework-order       - Criar retrabalho
GET    /quality/defects            - Histórico de defeitos
GET    /quality/reports            - Relatórios
```

### 7. Financial Service

**Responsabilidades:**
- Emitir notas fiscais
- Registrar pagamentos
- Gerar avisos de cobrança
- Calcular impostos

**Interfaces:**
```
POST   /invoices/generate          - Gerar NF-e
PUT    /invoices/:id/payment       - Registrar pagamento
GET    /invoices/overdue           - Faturas vencidas
GET    /financial/reports          - Relatórios financeiros
```

### 8. Customer Service

**Responsabilidades:**
- Gerenciar dados de clientes
- Manter histórico de pedidos
- Configurar descontos
- Registrar observações

**Interfaces:**
```
POST   /customers/create           - Criar cliente
GET    /customers/:id              - Obter cliente
GET    /customers/:id/orders       - Histórico de pedidos
PUT    /customers/:id/discount     - Configurar desconto
```

### 9. Delivery Service

**Responsabilidades:**
- Rastrear pedidos
- Registrar entregas
- Notificar atrasos
- Manter histórico de movimentação

**Interfaces:**
```
GET    /tracking/:code             - Rastrear pedido
POST   /delivery/complete          - Registrar entrega
GET    /delivery/status            - Status de entrega
```

### 10. HR Service

**Responsabilidades:**
- Gerenciar funcionários
- Configurar turnos
- Agendar pessoal
- Registrar horas trabalhadas

**Interfaces:**
```
POST   /employees/schedule         - Agendar funcionário
GET    /employees/:id/hours        - Horas trabalhadas
GET    /hr/productivity            - Relatórios de produtividade
```

### 11. Notification Service

**Responsabilidades:**
- Enviar notificações
- Gerenciar canais (email, SMS)
- Registrar histórico de notificações

**Interfaces:**
```
POST   /notifications/send         - Enviar notificação
GET    /notifications/history      - Histórico
```

### 12. Reporting Service

**Responsabilidades:**
- Gerar relatórios
- Criar dashboards
- Exportar dados
- Agregar métricas

**Interfaces:**
```
GET    /reports/orders             - Relatório de pedidos
GET    /reports/financial          - Relatório financeiro
GET    /dashboards/:id             - Dashboard customizado
POST   /reports/export             - Exportar relatório
```



---

## Data Models

### Diagrama ER (Entity-Relationship)

```
┌──────────────┐         ┌──────────────┐
│   Customer   │◄────────┤    Order     │
└──────────────┘         └──────────────┘
                                │
                                ├─────────────┐
                                │             │
                        ┌───────▼──────┐  ┌──▼──────────┐
                        │ ProductionOrder│  │ OrderItem  │
                        └───────┬──────┘  └────────────┘
                                │
                        ┌───────▼──────────┐
                        │ ProductionTask   │
                        └───────┬──────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼──┐  ┌─────▼──┐  ┌───▼────────┐
            │ Resource │  │Material │  │QualityCheck│
            └──────────┘  └────────┘  └────────────┘
                                │
                        ┌───────▼──────┐
                        │ MaterialReserve
                        └────────────────┘
```

### Entidades Principais

#### 1. Customer (Cliente)

```sql
CREATE TABLE customers (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20),
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(2),
  zip_code VARCHAR(10),
  tax_id VARCHAR(20) UNIQUE,
  credit_limit DECIMAL(12,2),
  payment_terms INT DEFAULT 30,
  discount_percentage DECIMAL(5,2) DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);
```

#### 2. Order (Pedido)

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(id),
  order_number VARCHAR(50) UNIQUE NOT NULL,
  status ENUM('draft', 'quoted', 'confirmed', 'in_production', 'completed', 'delivered', 'cancelled'),
  total_amount DECIMAL(12,2),
  discount_amount DECIMAL(12,2) DEFAULT 0,
  final_amount DECIMAL(12,2),
  requested_delivery_date DATE,
  estimated_delivery_date DATE,
  actual_delivery_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID NOT NULL,
  FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 3. OrderItem (Item do Pedido)

```sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  description VARCHAR(255) NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  subtotal DECIMAL(12,2) NOT NULL,
  format VARCHAR(50),
  paper_type VARCHAR(100),
  paper_weight INT,
  colors INT,
  finishing TEXT,
  file_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. ProductionOrder (Ordem de Produção)

```sql
CREATE TABLE production_orders (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  production_number VARCHAR(50) UNIQUE NOT NULL,
  status ENUM('pending', 'in_progress', 'completed', 'on_hold'),
  start_date TIMESTAMP,
  estimated_completion_date TIMESTAMP,
  actual_completion_date TIMESTAMP,
  total_time_minutes INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. ProductionTask (Tarefa de Produção)

```sql
CREATE TABLE production_tasks (
  id UUID PRIMARY KEY,
  production_order_id UUID NOT NULL REFERENCES production_orders(id),
  task_sequence INT NOT NULL,
  task_type ENUM('pre_print', 'print', 'finishing', 'quality', 'packaging'),
  status ENUM('pending', 'in_progress', 'completed', 'blocked'),
  assigned_resource_id UUID REFERENCES resources(id),
  assigned_employee_id UUID REFERENCES employees(id),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  duration_minutes INT,
  blocked_reason TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. Material (Insumo)

```sql
CREATE TABLE materials (
  id UUID PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  unit_of_measure ENUM('kg', 'unit', 'meter', 'liter'),
  unit_price DECIMAL(12,2) NOT NULL,
  supplier_id UUID REFERENCES suppliers(id),
  minimum_stock INT NOT NULL,
  maximum_stock INT NOT NULL,
  reorder_point INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 7. Inventory (Estoque)

```sql
CREATE TABLE inventory (
  id UUID PRIMARY KEY,
  material_id UUID NOT NULL UNIQUE REFERENCES materials(id),
  quantity_on_hand INT NOT NULL DEFAULT 0,
  quantity_reserved INT NOT NULL DEFAULT 0,
  quantity_available INT GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved),
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_received_date DATE,
  last_consumed_date DATE
);
```

#### 8. MaterialReserve (Reserva de Material)

```sql
CREATE TABLE material_reserves (
  id UUID PRIMARY KEY,
  production_order_id UUID NOT NULL REFERENCES production_orders(id),
  material_id UUID NOT NULL REFERENCES materials(id),
  quantity_reserved INT NOT NULL,
  quantity_consumed INT DEFAULT 0,
  status ENUM('reserved', 'partially_consumed', 'consumed', 'cancelled'),
  reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  consumed_at TIMESTAMP
);
```

#### 9. Resource (Recurso/Máquina)

```sql
CREATE TABLE resources (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  resource_type ENUM('printer', 'cutter', 'folder', 'binder', 'laminator'),
  capacity INT,
  speed_per_hour INT,
  status ENUM('available', 'in_use', 'maintenance', 'unavailable'),
  maintenance_schedule TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 10. ResourceSchedule (Agenda de Recursos)

```sql
CREATE TABLE resource_schedules (
  id UUID PRIMARY KEY,
  resource_id UUID NOT NULL REFERENCES resources(id),
  production_task_id UUID NOT NULL REFERENCES production_tasks(id),
  scheduled_start TIMESTAMP NOT NULL,
  scheduled_end TIMESTAMP NOT NULL,
  actual_start TIMESTAMP,
  actual_end TIMESTAMP,
  status ENUM('scheduled', 'in_progress', 'completed', 'cancelled'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 11. QualityCheck (Controle de Qualidade)

```sql
CREATE TABLE quality_checks (
  id UUID PRIMARY KEY,
  production_order_id UUID NOT NULL REFERENCES production_orders(id),
  check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  inspector_id UUID NOT NULL REFERENCES employees(id),
  result ENUM('approved', 'rejected', 'approved_with_remarks'),
  defect_type VARCHAR(255),
  defect_description TEXT,
  rework_required BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 12. Invoice (Nota Fiscal)

```sql
CREATE TABLE invoices (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  nfe_key VARCHAR(50),
  status ENUM('draft', 'issued', 'paid', 'overdue', 'cancelled'),
  issue_date DATE NOT NULL,
  due_date DATE NOT NULL,
  total_amount DECIMAL(12,2) NOT NULL,
  paid_amount DECIMAL(12,2) DEFAULT 0,
  payment_method ENUM('cash', 'check', 'card', 'transfer'),
  payment_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 13. Employee (Funcionário)

```sql
CREATE TABLE employees (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20),
  position VARCHAR(100),
  skills TEXT,
  hire_date DATE,
  status ENUM('active', 'inactive', 'on_leave'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 14. EmployeeSchedule (Agenda de Funcionários)

```sql
CREATE TABLE employee_schedules (
  id UUID PRIMARY KEY,
  employee_id UUID NOT NULL REFERENCES employees(id),
  production_task_id UUID NOT NULL REFERENCES production_tasks(id),
  scheduled_start TIMESTAMP NOT NULL,
  scheduled_end TIMESTAMP NOT NULL,
  actual_start TIMESTAMP,
  actual_end TIMESTAMP,
  hours_worked DECIMAL(5,2),
  status ENUM('scheduled', 'in_progress', 'completed', 'cancelled'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 15. Delivery (Entrega)

```sql
CREATE TABLE deliveries (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  tracking_code VARCHAR(50) UNIQUE NOT NULL,
  status ENUM('pending', 'in_transit', 'delivered', 'failed'),
  scheduled_delivery_date DATE,
  actual_delivery_date DATE,
  delivery_address TEXT,
  delivered_by VARCHAR(255),
  signature_url VARCHAR(500),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 16. User (Usuário do Sistema)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'manager', 'operator', 'salesperson', 'financial', 'quality'),
  is_active BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 17. AuditLog (Log de Auditoria)

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  entity_type VARCHAR(100) NOT NULL,
  entity_id UUID NOT NULL,
  action ENUM('create', 'update', 'delete', 'view'),
  old_values JSONB,
  new_values JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45)
);
```

