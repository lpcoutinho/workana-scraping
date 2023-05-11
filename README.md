# Workana Scraping Project
## O Problema
- Consultar os trabalhos publicados no Workana periodicamente
- Permitir fácil visualização e filtro dos dados
- Disponibilizar online as informações e análises tratadas

O projeto é desenvolvido em diversas etapas e para facilitar sua compreensão cada etapa está documentada e disponibilizada nesta estrutura.

A primeira atividade consiste em raspar os dados da plataforma Workana de modo que possa criar um DataSet para futuras análises.

Em [Road Map](#road-map) você pode verificar cada etapa e consultar sua documentação.

## A estrutura
O projeto for organizado para facilitar o acesso às informações e atividades desenvolvidas. Etapas e categorias de atividades estão dispostas em diretórios referentes a cada atividade.

Em ***docs/*** estão os documentos textuais desenvolvidos ao longo da atividade que explicam e justificam as metodologias utilizadas.

No diretório ***notebooks/*** ficarão disponíveis os arquivos ***jupyter*** que foram utilizados ao longo das atividades.

Os scripts e arquivos ***\*.py*** estarão no diretório ***workana_scrapp/***.

Enquanto os dados armazenados poderão ser acessados no diretório ***workana_scrapp/data***.

## Road Map
### Fase 1
1. [x] Extrair dados
    - [Scrap workana.com/jobs](/docs/scrap_workana.md)
2. [x] Armazenar e exportar dados
    - Dados armazenados e exportados em arquivos CSV
3. [x] Tratar
    - [Tratando as informações coletados](/docs/transform_data.md)

### Fase 2
- [ ] Telegram bot
- [ ] Minerar dados 
- [ ] Visualizar
- [ ] Disponibilizar

## To Do
-   [x] Makefile para formatar códigos
-   [ ] Pré-commit para formatar
-   [ ] Container Docker
-   [ ] Armazenar em PostgreSQL
-   [ ] Automatizar ezecução com Cron
-   [ ] Atualizar CSV com os dados extraidos
    -   [ ] Concatenar novos dados
    -   [ ] Atualizar coluna Bids  

## Dúvidas

As dúvidas relevantes que surgirem ao longo do trabalho serão armazenadas e discutidas em outro espaço. Para acessar [clique aqui](/docs/doubts.md) 