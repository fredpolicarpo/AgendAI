# Especificação de Produto: AgendAI
 - **Versão:** 1.0 
 - **Data:** 17 de maio de 2025 
 - **Autor:** Frederico Policarpo Martins Boaventura 

## 1. Introdução

O AgendAI é um assistente virtual inteligente, baseado em chatbot, projetado para simplificar e automatizar o processo de agendamento de compromissos para profissionais liberais e os seus clientes. Utilizando inteligência artificial generativa para uma comunicação natural e integrações com ferramentas Google (Calendar, Sheets, Gmail), o AgendAI visa otimizar a gestão de tempo, reduzir "no-shows" e melhorar a experiência de agendamento para ambas as partes. A interação com o AgendAI pode ser realizada tanto por texto quanto por voz.

## 2. Visão Geral e Problema

Profissionais liberais (médicos, advogados, consultores, terapeutas, etc.) frequentemente despendem tempo considerável na gestão manual de suas agendas, lidando com pedidos de agendamento, confirmações, cancelamentos e remarcações. Este processo pode ser ineficiente, propenso a erros e consumir tempo que poderia ser dedicado à sua atividade principal. Para os clientes, o processo de agendamento tradicional pode, por vezes, ser demorado e pouco flexível.

O AgendAI resolve estes problemas ao oferecer uma plataforma centralizada e automatizada que:

* Permite que clientes solicitem e gira os seus agendamentos de forma autónoma via chatbot.
* Permite que profissionais configurem a sua disponibilidade e giram os pedidos de agendamento através de uma interface conversacional.
* Automatiza notificações, lembretes e o fluxo de confirmação de agendamentos, incluindo políticas de cancelamento.
* Regista todas as interações para futuras consultas e relatórios.

## 3. Objetivos

* **Para Profissionais:**
    * Reduzir o tempo gasto na gestão manual de agendamentos.
    * Minimizar erros de agendamento.
    * Diminuir a taxa de não comparecimento (no-shows) através de lembretes e confirmações.
    * Oferecer uma visão clara e atualizada da sua agenda, com distinção visual para status de agendamento.
    * Permitir a configuração de políticas de cancelamento (limite de tempo e taxas).
    * Melhorar a eficiência operacional.
* **Para Clientes (Solicitantes):**
    * Proporcionar um processo de agendamento rápido, fácil e disponível 24/7.
    * Ser informado claramente sobre as políticas de cancelamento do profissional.
    * Oferecer flexibilidade para gerir os seus próprios agendamentos (cancelar, solicitar remarcação) ciente das condições.
    * Melhorar a experiência geral de interação com o profissional/serviço.
* **Gerais do Produto:**
    * Ser uma solução de referência para agendamento inteligente via chatbot.
    * Garantir alta precisão no reconhecimento de voz e processamento de linguagem natural.
    * Manter um tom de voz formal, educado, simpático e com leve entusiasmo em todas as interações.

## 4. Público-Alvo

* **Profissionais Liberais e Pequenas Empresas:** Advogados, médicos, dentistas, terapeutas, consultores, coaches, personal trainers, salões de beleza, estúdios, etc., que gerem os seus próprios agendamentos ou possuem uma pequena equipa para tal.
* **Clientes/Pacientes/Solicitantes:** Indivíduos que buscam agendar serviços com os profissionais acima.

## 5. Requisitos Funcionais (User Stories e Funcionalidades)

Todas as interações devem ser possíveis via **texto e voz**. O tom de voz do chatbot será **formal, educado, simpático e com leve entusiasmo**.

### P1: MVP Essencial – O Ciclo Completo via Chatbot

1.  **Configuração Inicial de Disponibilidade pelo Profissional:**
    * **User Story (Profissional):** "Como profissional, quero poder informar ao AgendAI os meus dias e horários de atendimento padrão, incluindo intervalos, para que o sistema saiba quando estou disponível."
    * **Funcionalidade:** O profissional, via chat (texto/voz), define a sua disponibilidade base (dias da semana, horários de início/fim, pausas). O AgendAI confirma e armazena essa estrutura, refletindo-a no Google Calendar do profissional (gerido pelo AgendAI).
        * **Exemplo de diálogo de configuração de disponibilidade:**
            * **AgendAI:** "Olá, \[Nome do Profissional\]! Para começarmos, por favor, diga-me quais dias da semana você geralmente atende. Por exemplo: 'segunda a sexta' ou 'segundas, quartas e sextas'."
            * **Profissional:** "Segunda a quinta."
            * **AgendAI:** "Entendido. E quais são os seus horários de atendimento nesses dias? Por exemplo: 'das 9h às 18h'."
            * **Profissional:** "Das 8h ao meio-dia e das 14h às 18h."
            * **AgendAI:** "Perfeito. Então sua disponibilidade base é de Segunda a Quinta, das 8h às 12h e das 14h às 18h. Correto?"
            * **Profissional:** "Correto."
            * **AgendAI:** "Ótimo! Sua disponibilidade foi configurada. ✨"
    * **Aceitação:** O profissional consegue definir a sua disponibilidade através de um diálogo guiado; o chatbot confirma a configuração; o Google Calendar do profissional reflete essa disponibilidade base.

2.  **Configuração da Política de Cancelamento pelo Profissional:**
    * **User Story (Profissional):** "Como profissional, quero poder definir um limite de tempo para cancelamento sem custos (ex: 2 horas antes) e o valor de uma taxa de cancelamento caso o cliente cancele após esse limite ou não compareça, para que o AgendAI possa informar e aplicar essa política."
    * **Funcionalidade:** O profissional, via chat (texto/voz), define o limite de antecedência para cancelamento gratuito (ex: "2 horas antes", "24 horas antes") e o valor da taxa de cancelamento (ex: "R$ 50,00"). O AgendAI armazena essa política.
        * **Exemplo de diálogo:**
            * **AgendAI:** "Gostaria de configurar uma política de cancelamento para os seus agendamentos? Isso pode incluir um prazo para cancelamento sem custos e uma taxa para cancelamentos tardios."
            * **Profissional:** "Sim, gostaria."
            * **AgendAI:** "Qual o prazo limite para cancelamento sem custos? Por exemplo, '2 horas antes' ou '1 dia antes'."
            * **Profissional:** "Até 24 horas antes."
            * **AgendAI:** "Entendido. E caso o cliente cancele após esse prazo, haverá alguma taxa de cancelamento? Se sim, qual o valor?"
            * **Profissional:** "Sim, uma taxa de 30 reais."
            * **AgendAI:** "Perfeito. Sua política de cancelamento foi configurada: cancelamentos com até 24 horas de antecedência são gratuitos. Após esse prazo, poderá ser aplicada uma taxa de R$ 30,00. Correto?"
            * **Profissional:** "Correto."
    * **Aceitação:** O profissional consegue definir o limite de tempo para cancelamento gratuito e o valor da taxa; o chatbot confirma a configuração da política.

3.  **Solicitação de Pré-Agendamento pelo Cliente:**
    * **User Story (Cliente):** "Como cliente, quero poder informar ao chatbot minhas preferências gerais de dia ou período (manhã, tarde, noite) antes de ver horários específicos, para que as opções sejam mais relevantes para mim, e quero ser informado sobre a política de cancelamento ao agendar."
    * **Funcionalidade:**
        1.  O cliente interage com o chatbot (texto/voz) para iniciar um agendamento (ex: "Gostaria de agendar uma consulta").
        2.  O chatbot, com base na disponibilidade configurada pelo profissional, pergunta ao cliente sobre suas preferências gerais: "Claro! Para o serviço de \[Nome do Serviço, se aplicável\], você tem alguma preferência de dia da semana ou período (manhã, tarde, noite)? Posso verificar as opções disponíveis em: \[listar apenas dias/períodos válidos, ex: 'Segundas à tarde', 'Terças de manhã', 'Qualquer dia da semana no período da manhã'\]."
        3.  O cliente informa sua preferência (ex: "Terça de manhã" ou "Qualquer dia à tarde").
        4.  O chatbot consulta a disponibilidade específica no Google Calendar do profissional, filtrando pelos dias/períodos que correspondem à preferência do cliente e à disponibilidade real do profissional.
        5.  O chatbot oferece os horários específicos disponíveis: "Para \[preferência do cliente, ex: 'Terça de manhã'\], tenho estes horários disponíveis: \[lista de horários\]. Qual deles você prefere?"
        6.  O cliente escolhe um horário.
        7.  **Informação sobre Política de Cancelamento (especialmente no primeiro agendamento ou conforme configuração):** Antes de finalizar o pré-agendamento, o chatbot informa: "Importante: \[Nome do Profissional\] possui uma política de cancelamento. Cancelamentos são aceitos sem custo com até \[limite de tempo configurado pelo profissional, ex: 24 horas\] de antecedência. Cancelamentos fora deste prazo ou não comparecimentos podem estar sujeitos a uma taxa de \[valor da taxa configurada, ex: R$ 30,00\]. Ao prosseguir, você concorda com esta política."
        8.  Neste momento (após o cliente estar ciente da política), um evento é criado no Google Calendar do profissional:
            * **Proprietário do Evento:** O profissional.
            * **Participantes:** O profissional e o cliente solicitante (se o e-mail do cliente for fornecido/conhecido).
            * **Título do Evento:** `[Pendente] - Nome do Serviço/Evento` (ex: `[Pendente] - Consulta Inicial`).
            * **Cor do Evento:** Laranja.
        9.  O chatbot informa o cliente: "Excelente! Seu pedido para \[data/hora escolhida\] foi enviado ao \[Nome do Profissional\] e aguarda confirmação. Avisaremos assim que tivermos uma resposta, tudo bem?"
    * **Aceitação:** O cliente consegue informar preferências gerais de dia/período; o chatbot apresenta opções de preferência válidas; o chatbot oferece horários específicos filtrados; o cliente é informado sobre a política de cancelamento antes da criação do pré-agendamento; um evento é criado no Google Calendar do profissional com título "\[Pendente\] - Nome do Evento", cor laranja; o pedido é registado como pré-agendamento.

4.  **Notificação e Gestão de Pré-Agendamento pelo Profissional:**
    * **User Story (Profissional):** "Como profissional, quero ser notificado pelo AgendAI sobre novos pedidos de pré-agendamento e poder confirmá-los ou rejeitá-los diretamente pelo chat, visualizando claramente o status pendente na minha agenda."
    * **Funcionalidade:** O profissional recebe uma notificação via chatbot sobre um novo pré-agendamento (detalhes do cliente, serviço, data/hora). O profissional pode "Confirmar" ou "Rejeitar" via chat (texto/voz ou botões de resposta rápida). O evento no Google Calendar já estará visível com o status pendente.
    * **Aceitação:** O profissional é notificado; consegue confirmar ou rejeitar o pedido; a ação é registada.

5.  **Atualização da Agenda e Notificação do Resultado ao Cliente:**
    * **User Story (Cliente):** "Como cliente, quero ser notificado pelo AgendAI se o meu pedido de agendamento foi confirmado ou rejeitado pelo profissional."
    * **User Story (Profissional):** "Como profissional, quero que ao confirmar um pré-agendamento, o evento no meu Google Calendar seja atualizado automaticamente para refletir o status de confirmado, mudando o título e a cor."
    * **Funcionalidade:**
        * **Se Confirmado:** O evento existente no Google Calendar do profissional é atualizado:
            * **Título do Evento:** Alterado para `[Confirmado] - Nome do Serviço/Evento` (ex: `[Confirmado] - Consulta Inicial`).
            * **Cor do Evento:** Alterada para Verde.
            O cliente é notificado da confirmação via chatbot.
        * **Se Rejeitado:** O evento pendente é removido do Google Calendar do profissional. O cliente é notificado da rejeição via chatbot e pode ser convidado a tentar um novo horário.
    * **Aceitação:** Se confirmado, o evento no Google Calendar é atualizado para título "\[Confirmado\] - Nome do Evento" e cor verde; o cliente recebe a notificação de confirmação. Se rejeitado, o evento é removido do Google Calendar; o cliente recebe a notificação de rejeição.

6.  **Consulta Simples de Agenda pelo Profissional:**
    * **User Story (Profissional):** "Como profissional, quero poder perguntar ao AgendAI sobre os meus compromissos para um dia específico ou período e receber um resumo, distinguindo visualmente os confirmados dos pendentes."
    * **Funcionalidade:** O profissional pergunta ao chatbot (texto/voz) sobre a sua agenda. O chatbot lê os eventos do Google Calendar do profissional (incluindo títulos e cores) e apresenta um resumo.
    * **Aceitação:** O profissional consegue consultar a sua agenda para datas futuras; o chatbot apresenta os compromissos corretos, permitindo a identificação do status pelo título/cor.

### P2: Melhorias Importantes – Ainda 100% via Chatbot

7.  **Atualização Dinâmica de Disponibilidade (Bloqueios/Desbloqueios) pelo Profissional:**
    * **User Story (Profissional):** "Como profissional, quero poder informar rapidamente ao AgendAI sobre bloqueios pontuais na minha agenda (ex: 'bloquear próxima terça das 14h às 16h') ou liberar horários previamente bloqueados."
    * **Funcionalidade:** O profissional, via chat (texto/voz), solicita bloqueios ou desbloqueios de horários específicos. O AgendAI confirma e atualiza o Google Calendar.
    * **Aceitação:** O profissional consegue bloquear/desbloquear horários; o GCalendar reflete as alterações.

8.  **Cancelamento de Agendamento Confirmado pelo Cliente (com Política de Cancelamento):**
    * **User Story (Cliente):** "Como cliente, quero poder cancelar um agendamento confirmado através do chatbot, sendo informado sobre possíveis taxas se o cancelamento for fora do prazo."
    * **Funcionalidade:**
        1.  O cliente informa ao chatbot o desejo de cancelar um agendamento.
        2.  O chatbot localiza o agendamento confirmado.
        3.  O chatbot verifica se o pedido de cancelamento está dentro do limite de tempo para cancelamento gratuito (definido pelo profissional).
            * **Se dentro do limite:** O chatbot pede confirmação: "Você confirma o cancelamento do seu agendamento para \[data/hora\]? Não haverá custos." Se o cliente confirmar, o evento (verde) é removido do Google Calendar e o profissional é notificado.
            * **Se fora do limite:** O chatbot informa: "Seu pedido de cancelamento para \[data/hora\] está fora do prazo permitido para cancelamento gratuito, que é de \[limite de tempo configurado\] de antecedência. Caso prossiga com o cancelamento, poderá ser aplicada uma taxa de \[valor da taxa configurada\]. Deseja continuar com o cancelamento? \[Sim, cancelar ciente da taxa\] \[Não, manter agendamento\]".
                * Se o cliente escolher "Sim, cancelar ciente da taxa": O evento (verde) é removido do Google Calendar, o profissional é notificado do cancelamento e da aplicabilidade da taxa. Um registro da intenção de cobrança da taxa é feito no Google Sheets.
                * Se o cliente escolher "Não, manter agendamento": O agendamento é mantido e o chatbot confirma: "Entendido. Seu agendamento para \[data/hora\] está mantido."
    * **Aceitação:** O cliente consegue solicitar o cancelamento; se o cancelamento estiver fora do prazo, o cliente é informado sobre a taxa e pode decidir se prossegue; o Google Calendar é atualizado conforme a decisão; o profissional é notificado; a possível cobrança de taxa é registrada no Google Sheets.

9.  **Notificação de Cancelamento (feito pelo Cliente) ao Profissional:**
    * **User Story (Profissional):** "Como profissional, quero ser notificado imediatamente pelo AgendAI quando um cliente cancelar um agendamento, incluindo se uma taxa de cancelamento é aplicável."
    * **Funcionalidade:** O chatbot notifica o profissional sobre o cancelamento realizado pelo cliente, indicando se o cancelamento ocorreu dentro ou fora do prazo e se a taxa de cancelamento é aplicável.
    * **Aceitação:** O profissional recebe a notificação de cancelamento em tempo hábil com informações sobre a política de cancelamento.

### P3: Funcionalidades Avançadas – Mantendo o Chatbot como Interface Única

10. **Lembretes Automáticos e Pedido de Confirmação de Comparecimento (Cliente e Profissional):**
    * **User Story (Profissional):** "Como profissional, quero poder configurar o AgendAI para enviar lembretes automáticos aos clientes X horas/dias antes do agendamento, solicitando a confirmação de comparecimento e relembrando a política de cancelamento."
    * **User Story (Cliente):** "Como cliente, quero receber um lembrete do meu agendamento, poder confirmar o meu comparecimento ou indicar a necessidade de reagendar/cancelar, e ser relembrado da política de cancelamento."
    * **Funcionalidade:** O profissional configura a política de lembretes via chat. O AgendAI envia automaticamente mensagens (via chatbot) aos clientes antes dos agendamentos (apenas para os confirmados - verdes), solicitando confirmação. **A mensagem de lembrete incluirá uma nota sobre a política de cancelamento:** "Olá, \[Nome do Cliente\]! Passando para lembrar do seu agendamento com \[Nome do Profissional\] em \[data\] às \[hora\]. Você confirma sua presença? \[Sim, confirmo\] \[Preciso Reagendar/Cancelar\]. Lembre-se que cancelamentos devem ser feitos com até \[limite de tempo configurado\] de antecedência para evitar a taxa de \[valor da taxa configurada\]."
        A resposta do cliente é registada e pode notificar o profissional. (A interação de cancelamento/reagendamento aqui seguirá a política de cancelamento).
    * **Aceitação:** Lembretes são enviados conforme configurado para eventos confirmados, incluindo a nota sobre a política de cancelamento; clientes conseguem confirmar/indicar ausência; o sistema regista a resposta.

11. **Relatórios Básicos para o Profissional (com base no GSheets):**
    * **User Story (Profissional):** "Como profissional, quero poder solicitar ao AgendAI relatórios simples, como o número de agendamentos confirmados numa semana, a taxa de cancelamento no último mês e o valor total de taxas de cancelamento aplicadas."
    * **Funcionalidade:** O profissional solicita relatórios básicos via chat (texto/voz). O AgendAI consulta os dados logados no Google Sheets (incluindo registros de taxas de cancelamento) e apresente os resumos.
    * **Aceitação:** O profissional consegue obter dados estatísticos básicos sobre os seus agendamentos e taxas.

## 6. Requisitos Não Funcionais

* **Usabilidade:** Interface conversacional intuitiva; respostas rápidas; clareza; tom de voz consistente.
* **Desempenho:**
    * Tempo de resposta do chatbot inferior a 5 segundos para a maioria das interações.
    * Capacidade para 150 clientes ativos por mês, com média de 12 agendamentos por dia.
    * Processamento eficiente de comandos de voz.
* **Confiabilidade:**
    * Alta precisão no agendamento e gestão de disponibilidade (evitar overbooking ou erros).
    * Disponibilidade do sistema de 99.5%.
    * Logs de todas as transações importantes para auditoria e recuperação.
* **Segurança:** Proteção de dados (LGPD); autenticação segura do profissional.
* **Manutenibilidade:** Código documentado e modular; fácil atualização.
* **Acessibilidade:** Suporte a texto e voz; (Futuro) WCAG.
* **Precisão do STT/PLN:** Alta precisão em português brasileiro; compreensão de intenções; tratamento de ambiguidades.

## 7. Integrações

* **Google Calendar:** Leitura de disponibilidade; CRUD de eventos (títulos, participantes, cores).
* **Google Sheets:** Logging (pedidos, confirmações, cancelamentos, configurações, erros, taxas aplicáveis). Fonte para relatórios.
* **Google Cloud Speech-to-Text (STT):** Conversão de voz para texto.
* **(Opcional/Futuro) Google Cloud Text-to-Speech (TTS):** Respostas por voz do chatbot.
* **(Opcional/Futuro) Gmail API:** Notificações por e-mail complementares.
* **Plataforma de Chatbot:** A definir (Dialogflow, etc.).

## 8. Considerações Técnicas

* **Motor de IA Generativa/PLN:** Flexibilidade e compreensão de intenções.
* **Gestão de Estado da Conversa:** Manter contexto.
* **Autenticação do Profissional:** Mecanismo seguro.
* **Interface do Chatbot:** Suporte a texto, STT, botões de resposta rápida.
* **Lógica de Disponibilidade e Política de Cancelamento:** Robusta para cruzar dados e aplicar regras.
* **Escalabilidade:** Arquitetura pensada para suportar o volume de 150 clientes ativos/mês e uma média de 12 agendamentos/dia, garantindo o tempo de resposta de até 5s.
* **API do Google Calendar:** Uso das funcionalidades para gestão de eventos.

## 9. Métricas de Sucesso

* **Adoção:** Nº de profissionais ativos; Nº de clientes utilizando.
* **Engajamento:** Nº de agendamentos/período; Frequência de uso pelos profissionais.
* **Eficiência:** Redução tempo médio de agendamento; Taxa de sucesso do chatbot; Taxa de uso de voz.
* **Satisfação:** Feedback qualitativo; Redução de "no-shows"; Taxa de cancelamento dentro/fora do prazo.
* **Técnicas:** Precisão STT/PLN; Tempo de atividade (uptime) conforme SLA de 99.5%; Tempo de resposta do sistema dentro do SLA.

## 10. Escopo Futuro / Fora do Escopo (MVP Inicial)

* Pagamentos integrados (incluindo cobrança automática de taxas de cancelamento).
* Gestão de múltiplos profissionais/locais.
* Integração com outros calendários.
* Relatórios avançados.
* Personalização avançada do chatbot.
* Respostas por voz (TTS).
* Campanha de marketing.
* App móvel dedicado.