-- Initialize ERP Database Schema
-- This script creates the initial database structure for ERP Gráficas Expressas

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================
-- USERS & AUTH
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'operator',
  is_active BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45)
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- ============================================================
-- CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_tax_id ON customers(tax_id);
CREATE INDEX IF NOT EXISTS idx_customers_name ON customers USING gin(name gin_trgm_ops);

-- ============================================================
-- ORDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  customer_id UUID NOT NULL REFERENCES customers(id),
  order_number VARCHAR(50) UNIQUE NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  total_amount DECIMAL(12,2),
  discount_amount DECIMAL(12,2) DEFAULT 0,
  final_amount DECIMAL(12,2),
  requested_delivery_date DATE,
  estimated_delivery_date DATE,
  actual_delivery_date DATE,
  notes TEXT,
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT orders_status_check CHECK (status IN ('draft','quoted','confirmed','in_production','completed','delivered','cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_order_number ON orders(order_number);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

-- Order Items
CREATE TABLE IF NOT EXISTS order_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
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

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- ============================================================
-- EMPLOYEES
-- ============================================================

CREATE TABLE IF NOT EXISTS employees (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20),
  position VARCHAR(100),
  skills TEXT,
  hire_date DATE,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT employees_status_check CHECK (status IN ('active','inactive','on_leave'))
);

CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);

-- ============================================================
-- RESOURCES (MACHINES)
-- ============================================================

CREATE TABLE IF NOT EXISTS resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  resource_type VARCHAR(50) NOT NULL,
  capacity INT,
  speed_per_hour INT,
  status VARCHAR(20) NOT NULL DEFAULT 'available',
  maintenance_schedule TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT resources_type_check CHECK (resource_type IN ('printer','cutter','folder','binder','laminator')),
  CONSTRAINT resources_status_check CHECK (status IN ('available','in_use','maintenance','unavailable'))
);

CREATE INDEX IF NOT EXISTS idx_resources_status ON resources(status);
CREATE INDEX IF NOT EXISTS idx_resources_type ON resources(resource_type);

-- ============================================================
-- PRODUCTION
-- ============================================================

CREATE TABLE IF NOT EXISTS production_orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID NOT NULL REFERENCES orders(id),
  production_number VARCHAR(50) UNIQUE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  start_date TIMESTAMP,
  estimated_completion_date TIMESTAMP,
  actual_completion_date TIMESTAMP,
  total_time_minutes INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT production_orders_status_check CHECK (status IN ('pending','in_progress','completed','on_hold'))
);

CREATE INDEX IF NOT EXISTS idx_production_orders_order_id ON production_orders(order_id);
CREATE INDEX IF NOT EXISTS idx_production_orders_status ON production_orders(status);

CREATE TABLE IF NOT EXISTS production_tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  production_order_id UUID NOT NULL REFERENCES production_orders(id) ON DELETE CASCADE,
  task_sequence INT NOT NULL,
  task_type VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  assigned_resource_id UUID REFERENCES resources(id),
  assigned_employee_id UUID REFERENCES employees(id),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  duration_minutes INT,
  blocked_reason TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT production_tasks_type_check CHECK (task_type IN ('pre_print','print','finishing','quality','packaging')),
  CONSTRAINT production_tasks_status_check CHECK (status IN ('pending','in_progress','completed','blocked'))
);

CREATE INDEX IF NOT EXISTS idx_production_tasks_production_order_id ON production_tasks(production_order_id);
CREATE INDEX IF NOT EXISTS idx_production_tasks_status ON production_tasks(status);
CREATE INDEX IF NOT EXISTS idx_production_tasks_resource_id ON production_tasks(assigned_resource_id);
CREATE INDEX IF NOT EXISTS idx_production_tasks_employee_id ON production_tasks(assigned_employee_id);

-- ============================================================
-- MATERIALS & INVENTORY
-- ============================================================

CREATE TABLE IF NOT EXISTS materials (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  unit_of_measure VARCHAR(20) NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  minimum_stock INT NOT NULL,
  maximum_stock INT NOT NULL,
  reorder_point INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT materials_uom_check CHECK (unit_of_measure IN ('kg','unit','meter','liter'))
);

CREATE INDEX IF NOT EXISTS idx_materials_code ON materials(code);
CREATE INDEX IF NOT EXISTS idx_materials_name ON materials USING gin(name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS inventory (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  material_id UUID NOT NULL UNIQUE REFERENCES materials(id),
  quantity_on_hand INT NOT NULL DEFAULT 0,
  quantity_reserved INT NOT NULL DEFAULT 0,
  quantity_available INT GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_received_date DATE,
  last_consumed_date DATE
);

CREATE INDEX IF NOT EXISTS idx_inventory_material_id ON inventory(material_id);

CREATE TABLE IF NOT EXISTS material_reserves (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  production_order_id UUID NOT NULL REFERENCES production_orders(id),
  material_id UUID NOT NULL REFERENCES materials(id),
  quantity_reserved INT NOT NULL,
  quantity_consumed INT DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'reserved',
  reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  consumed_at TIMESTAMP,
  CONSTRAINT material_reserves_status_check CHECK (status IN ('reserved','partially_consumed','consumed','cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_material_reserves_production_order_id ON material_reserves(production_order_id);
CREATE INDEX IF NOT EXISTS idx_material_reserves_material_id ON material_reserves(material_id);
CREATE INDEX IF NOT EXISTS idx_material_reserves_status ON material_reserves(status);

-- ============================================================
-- RESOURCE SCHEDULES
-- ============================================================

CREATE TABLE IF NOT EXISTS resource_schedules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  resource_id UUID NOT NULL REFERENCES resources(id),
  production_task_id UUID NOT NULL REFERENCES production_tasks(id),
  scheduled_start TIMESTAMP NOT NULL,
  scheduled_end TIMESTAMP NOT NULL,
  actual_start TIMESTAMP,
  actual_end TIMESTAMP,
  status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT resource_schedules_status_check CHECK (status IN ('scheduled','in_progress','completed','cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_resource_schedules_resource_id ON resource_schedules(resource_id);
CREATE INDEX IF NOT EXISTS idx_resource_schedules_task_id ON resource_schedules(production_task_id);
CREATE INDEX IF NOT EXISTS idx_resource_schedules_start ON resource_schedules(scheduled_start);

-- ============================================================
-- EMPLOYEE SCHEDULES
-- ============================================================

CREATE TABLE IF NOT EXISTS employee_schedules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  employee_id UUID NOT NULL REFERENCES employees(id),
  production_task_id UUID NOT NULL REFERENCES production_tasks(id),
  scheduled_start TIMESTAMP NOT NULL,
  scheduled_end TIMESTAMP NOT NULL,
  actual_start TIMESTAMP,
  actual_end TIMESTAMP,
  hours_worked DECIMAL(5,2),
  status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT employee_schedules_status_check CHECK (status IN ('scheduled','in_progress','completed','cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_employee_schedules_employee_id ON employee_schedules(employee_id);
CREATE INDEX IF NOT EXISTS idx_employee_schedules_task_id ON employee_schedules(production_task_id);

-- ============================================================
-- QUALITY CHECKS
-- ============================================================

CREATE TABLE IF NOT EXISTS quality_checks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  production_order_id UUID NOT NULL REFERENCES production_orders(id),
  check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  inspector_id UUID NOT NULL REFERENCES employees(id),
  result VARCHAR(30) NOT NULL,
  defect_type VARCHAR(255),
  defect_description TEXT,
  rework_required BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT quality_checks_result_check CHECK (result IN ('approved','rejected','approved_with_remarks'))
);

CREATE INDEX IF NOT EXISTS idx_quality_checks_production_order_id ON quality_checks(production_order_id);
CREATE INDEX IF NOT EXISTS idx_quality_checks_result ON quality_checks(result);
CREATE INDEX IF NOT EXISTS idx_quality_checks_check_date ON quality_checks(check_date);

-- ============================================================
-- INVOICES
-- ============================================================

CREATE TABLE IF NOT EXISTS invoices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID NOT NULL REFERENCES orders(id),
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  nfe_key VARCHAR(50),
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  issue_date DATE NOT NULL,
  due_date DATE NOT NULL,
  total_amount DECIMAL(12,2) NOT NULL,
  paid_amount DECIMAL(12,2) DEFAULT 0,
  payment_method VARCHAR(20),
  payment_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT invoices_status_check CHECK (status IN ('draft','issued','paid','overdue','cancelled')),
  CONSTRAINT invoices_payment_method_check CHECK (payment_method IS NULL OR payment_method IN ('cash','check','card','transfer'))
);

CREATE INDEX IF NOT EXISTS idx_invoices_order_id ON invoices(order_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date);

-- ============================================================
-- DELIVERIES
-- ============================================================

CREATE TABLE IF NOT EXISTS deliveries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID NOT NULL REFERENCES orders(id),
  tracking_code VARCHAR(50) UNIQUE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  scheduled_delivery_date DATE,
  actual_delivery_date DATE,
  delivery_address TEXT,
  delivered_by VARCHAR(255),
  signature_url VARCHAR(500),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT deliveries_status_check CHECK (status IN ('pending','in_transit','delivered','failed'))
);

CREATE INDEX IF NOT EXISTS idx_deliveries_order_id ON deliveries(order_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_tracking_code ON deliveries(tracking_code);
CREATE INDEX IF NOT EXISTS idx_deliveries_status ON deliveries(status);

-- ============================================================
-- NOTIFICATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT,
  data JSONB,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);

-- ============================================================
-- AUDIT LOGS
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id),
  entity_type VARCHAR(100) NOT NULL,
  entity_id UUID NOT NULL,
  action VARCHAR(20) NOT NULL,
  old_values JSONB,
  new_values JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45),
  CONSTRAINT audit_logs_action_check CHECK (action IN ('create','update','delete','view'))
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);

-- ============================================================
-- BACKUP METADATA
-- ============================================================

CREATE TABLE IF NOT EXISTS backup_metadata (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  backup_name VARCHAR(255) NOT NULL,
  backup_type VARCHAR(50) NOT NULL DEFAULT 'full',
  status VARCHAR(20) NOT NULL,
  size_bytes BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  error_message TEXT,
  retention_until TIMESTAMP,
  CONSTRAINT backup_metadata_status_check CHECK (status IN ('running','success','failed'))
);

CREATE INDEX IF NOT EXISTS idx_backup_metadata_created_at ON backup_metadata(created_at);
CREATE INDEX IF NOT EXISTS idx_backup_metadata_status ON backup_metadata(status);

-- ============================================================
-- PERMISSIONS
-- ============================================================

DO $$
BEGIN
  IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'erp_user') THEN
    GRANT CONNECT ON DATABASE erp_grafica TO erp_user;
    GRANT USAGE ON SCHEMA public TO erp_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO erp_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO erp_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO erp_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO erp_user;
  END IF;
END
$$;
