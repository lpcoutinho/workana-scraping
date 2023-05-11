# Dúvidas 

Existem várias etapas no desenvolver do projeto, aqui discreverei dúvidas e questionamentos que surgirem ao longo do desenvolvimento. 

Cada tópico fará referência a determinada parte do projeto e referenciado ao longo da documentação.

## Workana scrap

### Script falhando nas primeiras vezes
#### Observações
- Falhas ao rodar o script pela primeira vez. Em alguns momentos preciso rodar 3 vezes ou mais para que o scrap seja concluido com sucesso.
- Por padrão a sessão inicia em tela pequena e ocorrem erros.
#### Questões
- O script estaria rodando muito rápido a ponto de tentar ler as informações antes que ela esteja completamente disponíveis?
- O script está muito rápido?
- Serei penalizado pela quatidade de requisições caso itere por todas as páginas de jobs?
- Usar WebDriverWait melhora?
- Usar time.sleep() melhora?

#### Proposições
- Iniciar sessão em tela maximizada.
- Usar WebDriverWait nas coletas de dados
- Usar time.sleep() melhora?
#### Testes
- Tela maximizada aparentemente apresenta menores taxas de erro.
- time.sleep(15) para trocar de página sugere usuabilidade humana. 
#### Implementações
- Iniciar sessão em tela maximizada.
- time.sleep() ao trocar de página.