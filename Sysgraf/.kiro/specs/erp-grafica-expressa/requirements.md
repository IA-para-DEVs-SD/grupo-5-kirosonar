# Documento de Requisitos - ERP para Gráficas Expressas

## Introdução

Este documento especifica os requisitos de negócio para um Sistema ERP integrado destinado a gráficas expressas. O sistema deve gerenciar o ciclo completo de operações de uma gráfica, desde a recepção de pedidos até a entrega final, incluindo gestão de materiais, produção, financeiro e relacionamento com clientes. O foco é em operações de alta velocidade com prazos curtos e demanda por flexibilidade operacional.

## Glossário

- **Sistema**: O ERP para Gráficas Expressas
- **Pedido**: Solicitação de impressão com especificações técnicas, quantidade e prazo
- **Orçamento**: Proposta de preço e prazo para um pedido
- **Especificação Técnica**: Detalhes de impressão (formato, cores, acabamento, papel, etc.)
- **Insumo**: Material consumível (papel, tinta, verniz, etc.)
- **Estoque**: Quantidade disponível de insumos e produtos acabados
- **Fluxo de Produção**: Sequência de etapas de processamento de um pedido
- **Ordem de Produção**: Instrução de fabricação gerada a partir de um pedido confirmado
- **Cliente**: Pessoa jurídica ou física que solicita serviços de impressão
- **Faturamento**: Processo de emissão de nota fiscal e cobrança
- **Recurso**: Máquina, equipamento ou pessoa disponível para produção
- **Agendamento**: Alocação de recursos para execução de tarefas
- **Controle de Qualidade**: Verificação de conformidade do produto com especificações
- **Acabamento**: Processos pós-impressão (corte, dobra, encadernação, etc.)

## Requisitos

### Requisito 1: Gestão de Pedidos e Orçamentos

**User Story:** Como gerente de vendas, quero criar orçamentos e pedidos de impressão com especificações técnicas detalhadas, para que eu possa oferecer propostas precisas aos clientes e gerenciar a produção.

#### Critérios de Aceitação

1. WHEN um cliente solicita um orçamento, THE Sistema SHALL capturar formato, quantidade, tipo de papel, número de cores, acabamentos e prazo desejado
2. THE Sistema SHALL calcular automaticamente o preço do orçamento com base em tabelas de custos configuráveis
3. WHEN um orçamento é aprovado pelo cliente, THE Sistema SHALL converter automaticamente para um Pedido confirmado
4. WHEN um Pedido é criado, THE Sistema SHALL gerar uma Ordem de Produção com todas as especificações técnicas
5. IF um cliente solicita alterações em um Pedido já confirmado, THEN THE Sistema SHALL registrar as alterações e recalcular prazos e custos
6. THE Sistema SHALL manter histórico de todos os Orçamentos e Pedidos com datas de criação, modificação e status

### Requisito 2: Gestão de Especificações Técnicas de Impressão

**User Story:** Como operador de produção, quero acessar especificações técnicas detalhadas de cada pedido, para que eu possa configurar corretamente as máquinas de impressão.

#### Critérios de Aceitação

1. THE Sistema SHALL armazenar para cada Pedido: dimensões finais, dimensões de sangria, número de cores, tipo de papel, gramatura, acabamentos (corte, dobra, encadernação, laminação, verniz)
2. WHEN uma Ordem de Produção é criada, THE Sistema SHALL exibir as especificações técnicas de forma clara e acessível aos operadores
3. THE Sistema SHALL permitir anexar arquivos de arte (PDF, imagens) às especificações técnicas
4. WHEN um operador inicia a produção, THE Sistema SHALL registrar o timestamp de início
5. IF especificações técnicas forem alteradas após o início da produção, THEN THE Sistema SHALL notificar o operador e registrar a alteração

### Requisito 3: Gestão de Materiais e Insumos

**User Story:** Como gerente de materiais, quero controlar o estoque de papéis, tintas e outros insumos, para que eu possa evitar falta de materiais e otimizar custos.

#### Critérios de Aceitação

1. THE Sistema SHALL manter registro de todos os Insumos com código, descrição, unidade de medida, preço unitário e fornecedor
2. WHEN um Insumo é recebido, THE Sistema SHALL atualizar automaticamente o Estoque com a quantidade recebida
3. WHEN uma Ordem de Produção é criada, THE Sistema SHALL reservar automaticamente os Insumos necessários do Estoque
4. IF a quantidade de um Insumo cair abaixo do nível mínimo configurado, THEN THE Sistema SHALL gerar um alerta de reposição
5. THE Sistema SHALL permitir configurar níveis mínimos e máximos de Estoque por Insumo
6. WHEN um Insumo é consumido na produção, THE Sistema SHALL registrar a quantidade consumida e atualizar o Estoque
7. THE Sistema SHALL calcular automaticamente o custo de Insumos para cada Pedido

### Requisito 4: Fluxo de Produção e Ordens de Trabalho

**User Story:** Como supervisor de produção, quero gerenciar o fluxo de trabalho de cada pedido através das etapas de produção, para que eu possa garantir prazos e qualidade.

#### Critérios de Aceitação

1. THE Sistema SHALL permitir definir etapas de produção customizáveis (pré-impressão, impressão, acabamento, qualidade, embalagem)
2. WHEN uma Ordem de Produção é criada, THE Sistema SHALL criar automaticamente tarefas para cada etapa de produção
3. WHEN um operador conclui uma etapa, THE Sistema SHALL registrar o timestamp de conclusão e permitir transição para a próxima etapa
4. IF uma etapa não pode ser iniciada (falta de Insumos ou Recursos), THEN THE Sistema SHALL bloquear a transição e exibir o motivo
5. THE Sistema SHALL exibir visualmente o progresso de cada Pedido através do fluxo de produção
6. WHEN uma Ordem de Produção é concluída, THE Sistema SHALL registrar o tempo total de produção e comparar com o prazo estimado

### Requisito 5: Agendamento de Recursos e Máquinas

**User Story:** Como gerente de produção, quero agendar máquinas e recursos para pedidos, para que eu possa otimizar a utilização de equipamentos e cumprir prazos.

#### Critérios de Aceitação

1. THE Sistema SHALL manter registro de todos os Recursos (máquinas, equipamentos) com capacidade, velocidade e tipos de trabalho que podem executar
2. WHEN uma Ordem de Produção é criada, THE Sistema SHALL sugerir automaticamente Recursos disponíveis com base nas especificações técnicas
3. THE Sistema SHALL permitir agendar manualmente Recursos para tarefas específicas
4. IF um Recurso está indisponível no período solicitado, THEN THE Sistema SHALL exibir alternativas disponíveis
5. WHEN um Recurso é alocado a uma tarefa, THE Sistema SHALL bloquear sua disponibilidade para outros Pedidos no período
6. THE Sistema SHALL exibir um calendário visual de utilização de Recursos
7. WHEN um Recurso falha ou fica indisponível, THE Sistema SHALL permitir reagendar automaticamente as tarefas afetadas

### Requisito 6: Gestão de Clientes e Relacionamento

**User Story:** Como gerente de contas, quero manter informações detalhadas de clientes e histórico de pedidos, para que eu possa oferecer melhor atendimento e identificar oportunidades de venda.

#### Critérios de Aceitação

1. THE Sistema SHALL manter registro de cada Cliente com nome, contato, endereço, dados fiscais e limite de crédito
2. THE Sistema SHALL armazenar histórico completo de Pedidos, Orçamentos e transações financeiras por Cliente
3. WHEN um Cliente solicita um novo Orçamento, THE Sistema SHALL exibir seu histórico de pedidos anteriores
4. THE Sistema SHALL permitir configurar descontos específicos por Cliente ou por volume
5. WHEN um Cliente tem atraso em pagamento, THE Sistema SHALL alertar o gerente de contas
6. THE Sistema SHALL permitir anexar notas e observações a cada Cliente

### Requisito 7: Faturamento e Gestão Financeira

**User Story:** Como gerente financeiro, quero emitir notas fiscais, controlar recebimentos e gerar relatórios financeiros, para que eu possa manter a saúde financeira da empresa.

#### Critérios de Aceitação

1. WHEN um Pedido é concluído e entregue, THE Sistema SHALL gerar automaticamente uma Nota Fiscal eletrônica
2. THE Sistema SHALL integrar com sistemas de emissão de NF-e (conforme legislação brasileira)
3. THE Sistema SHALL permitir configurar diferentes formas de pagamento (dinheiro, cheque, cartão, transferência)
4. WHEN um pagamento é recebido, THE Sistema SHALL registrar e marcar a Nota Fiscal como quitada
5. IF uma Nota Fiscal não é paga no prazo, THEN THE Sistema SHALL gerar automaticamente um aviso de cobrança
6. THE Sistema SHALL gerar relatórios de fluxo de caixa, contas a receber e contas a pagar
7. THE Sistema SHALL permitir configurar impostos e taxas por tipo de serviço

### Requisito 8: Controle de Qualidade

**User Story:** Como inspetor de qualidade, quero registrar verificações de qualidade em cada etapa de produção, para que eu possa garantir conformidade com especificações.

#### Critérios de Aceitação

1. WHEN uma Ordem de Produção atinge a etapa de Controle de Qualidade, THE Sistema SHALL exibir os critérios de aceitação baseados nas especificações técnicas
2. THE Sistema SHALL permitir registrar resultado de inspeção (aprovado, reprovado, aprovado com ressalvas)
3. IF um Pedido é reprovado no Controle de Qualidade, THEN THE Sistema SHALL criar automaticamente uma Ordem de Retrabalho
4. THE Sistema SHALL manter histórico de rejeições por tipo de defeito
5. WHEN um Pedido é aprovado no Controle de Qualidade, THE Sistema SHALL liberar para embalagem e entrega
6. THE Sistema SHALL gerar relatórios de taxa de rejeição e defeitos mais comuns

### Requisito 9: Gestão de Recursos Humanos e Agendamento

**User Story:** Como gerente de RH, quero gerenciar horários, turnos e alocação de pessoal, para que eu possa otimizar a produção e cumprir prazos.

#### Critérios de Aceitação

1. THE Sistema SHALL manter registro de cada Funcionário com dados pessoais, cargo, habilidades e disponibilidade
2. THE Sistema SHALL permitir configurar turnos e horários de trabalho
3. WHEN uma Ordem de Produção é criada, THE Sistema SHALL sugerir Funcionários com habilidades necessárias
4. THE Sistema SHALL permitir agendar Funcionários para tarefas específicas
5. IF um Funcionário não está disponível, THEN THE Sistema SHALL sugerir alternativas
6. THE Sistema SHALL registrar horas trabalhadas por Funcionário e por Pedido
7. THE Sistema SHALL gerar relatórios de produtividade por Funcionário

### Requisito 10: Rastreamento e Entrega

**User Story:** Como gerente de logística, quero rastrear pedidos desde a produção até a entrega, para que eu possa informar clientes sobre status e garantir entregas no prazo.

#### Critérios de Aceitação

1. WHEN uma Ordem de Produção é criada, THE Sistema SHALL atribuir um código de rastreamento único
2. THE Sistema SHALL permitir que Clientes consultem o status de seus Pedidos em tempo real
3. WHEN um Pedido é concluído, THE Sistema SHALL registrar a data de conclusão e preparar para embalagem
4. WHEN um Pedido é entregue, THE Sistema SHALL registrar data, hora e responsável pela entrega
5. IF um Pedido não será entregue no prazo estimado, THEN THE Sistema SHALL notificar automaticamente o Cliente
6. THE Sistema SHALL manter histórico completo de movimentação de cada Pedido

### Requisito 11: Relatórios e Análises

**User Story:** Como diretor, quero acessar relatórios e dashboards com indicadores de desempenho, para que eu possa tomar decisões estratégicas.

#### Critérios de Aceitação

1. THE Sistema SHALL gerar relatórios de volume de pedidos por período
2. THE Sistema SHALL calcular e exibir taxa de cumprimento de prazos
3. THE Sistema SHALL gerar relatórios de rentabilidade por Cliente e por tipo de serviço
4. THE Sistema SHALL exibir indicadores de utilização de Recursos e máquinas
5. THE Sistema SHALL gerar relatórios de custo de produção versus preço de venda
6. THE Sistema SHALL permitir exportar relatórios em formatos padrão (PDF, Excel)
7. THE Sistema SHALL permitir criar dashboards customizados com indicadores selecionados

### Requisito 12: Integração e Importação de Dados

**User Story:** Como administrador do sistema, quero importar dados de clientes, produtos e histórico de pedidos, para que eu possa migrar de sistemas legados.

#### Critérios de Aceitação

1. THE Sistema SHALL permitir importar dados de Clientes a partir de arquivos CSV ou Excel
2. THE Sistema SHALL permitir importar histórico de Pedidos de sistemas anteriores
3. WHEN dados são importados, THE Sistema SHALL validar integridade e exibir erros de importação
4. IF erros são encontrados durante importação, THEN THE Sistema SHALL permitir corrigir e reimportar
5. THE Sistema SHALL manter log de todas as importações realizadas

### Requisito 13: Segurança e Controle de Acesso

**User Story:** Como administrador de TI, quero controlar quem pode acessar cada funcionalidade do sistema, para que eu possa proteger dados sensíveis.

#### Critérios de Aceitação

1. THE Sistema SHALL implementar autenticação com usuário e senha
2. THE Sistema SHALL permitir definir papéis (gerente, operador, vendedor, financeiro, etc.)
3. WHEN um usuário tenta acessar uma funcionalidade, THE Sistema SHALL verificar se tem permissão baseado em seu papel
4. THE Sistema SHALL registrar todas as ações de usuários em um log de auditoria
5. IF um usuário tenta acessar dados não autorizados, THEN THE Sistema SHALL bloquear e registrar a tentativa
6. THE Sistema SHALL permitir resetar senhas de usuários

### Requisito 14: Notificações e Alertas

**User Story:** Como operador, quero receber notificações sobre eventos importantes, para que eu possa reagir rapidamente a problemas.

#### Critérios de Aceitação

1. WHEN um Pedido está próximo do prazo de entrega, THE Sistema SHALL enviar notificação ao supervisor
2. WHEN um Insumo atinge nível mínimo de Estoque, THE Sistema SHALL notificar o gerente de materiais
3. WHEN um Recurso fica indisponível, THE Sistema SHALL notificar o gerente de produção
4. WHEN um Pedido é reprovado no Controle de Qualidade, THE Sistema SHALL notificar o supervisor de produção
5. THE Sistema SHALL permitir configurar canais de notificação (email, SMS, notificação no sistema)

### Requisito 15: Backup e Recuperação de Dados

**User Story:** Como administrador de TI, quero garantir que dados do sistema sejam protegidos contra perda, para que eu possa recuperar informações em caso de falha.

#### Critérios de Aceitação

1. THE Sistema SHALL realizar backups automáticos diariamente
2. THE Sistema SHALL permitir restaurar dados a partir de um backup anterior
3. WHEN um backup é realizado, THE Sistema SHALL registrar data, hora e status
4. THE Sistema SHALL manter pelo menos 30 dias de histórico de backups
5. IF um backup falha, THEN THE Sistema SHALL notificar o administrador

