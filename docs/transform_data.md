# Tratamento de dados
Aqui basicamente utilizaremos a biblioteca ***Pandas*** para fazer todo trabalho. Esta biblioteca fornece estruturas eficientes para atuar em dados tabulares como tabelas e planilhas.

Além disso, o ***Pandas*** também oferece uma variedade de ferramentas para manipulação e limpeza de dados, como a remoção de valores nulos e a transformação de dados.

## Importando os dados
Antes da mais nada precisamos importar a biblioteca e os dados em que queremos trabalhar.

```python
import pandas as pd

df_raw = pd.read_csv('../workana_scrapp/data/data_raw.csv')

# check shape
df_raw.shape
```
## Copiando o DataFrame original
Por segurança copio o dataframe original. Desta forma preservamos os dados extraidos e utilizamos um novo dataframe para realizar testes e análises. Sempre que preciso posso criar um novo dataframe a partir do original sem risco de qualquer perda de dados.

```python
# create a copy
df = df_raw.copy()
```

## Conhecendo os dados
Com o novo dataframe criado preciso tratar as informações de modo que sejam melhores aproveitadas pelo Python. Começo verificando tamanho, tipos de dados e se existem valores nulos disponíveis no dataframe.

Você pode fazer isso manualmente com os métodos `pd.shape`, `pd.count()` e `pd.dtypes` ou usar `pd.info()` que retorna todas estas informações de uma única vez.

```python
df.info()
```

```python
# dataframe shape
print(df.shape)
```

```python
# column types
print(df.dtypes)
```

```python
# search for null values
# df.shape = (9, 7)
for c in df.columns:
    try:
        num_nulls = df.shape[0] - df[c].count()
        print(f'Valores nulos em {c}:',num_nulls)
    except:
        print(f'Erros encontrados em: {c}')
```

Agora verifico onde existem valores únicos para futura análise.
```python
# check if column has unique values
vu=[]
vr=[]
for c in df.columns:
    try:
        df[c].is_unique
        if df[c].is_unique == True:
            vu.append(c)
        else:
            vr.append(c)
    except:
        print(f'Erros encontrados em: {c}')

print(f'Valores únicos em: {vu}')
print(f'Valores repetem em: {vr}')
```

## Alterando os tipos de dados
Para melhorar a performance da nossa análise precisamos alterar a coluna ***Publish Date*** para o tipo datetime, enquanto ***Bids*** será um tipo numérico.

Implementei no código um tratamento de erro, quando não forem encontrados os itens solicitados uma mensagem de erro é adicionada ao campo não encontrado para aquela linha do dataframe.

Caso encontre erro como o mencionado acima remova a linha.

```python
# if error, drop line
df = df.drop(df[df['Bids'] == 'Erro no orçamento 10 da página5'].index)
```

### Bids
Quando realizamos a raspagem de dados e criamos um dataframe é possível observar que a coluna ***Bids*** é exibida como um tipo object. Isso  ocorre porque o Python a captura como string e não reconhece o tipo numérico. 

Porém, se você exportar os dados para um arquivo ***.csv*** e importar este arquivo em outro dataframe observará que esta coluna já apresenta o tipo inteiro.

Desse modo, caso você execute o projeto como eu não será preciso transformar os dados desta coluna.

```python
# change Bids to int type
df['Bids'] = df['Bids'].astype(int)
```
### Publish Date
Como as datas estão em padrão brasileiro de escrita tive alguma dificuldade em converter esta coluna. Para isso precisei criar um dicionário com os valores dos meses em português e inglês para converter as datas na coluna.

```python
months = {
    'Janeiro': 'January',
    'Fevereiro': 'February',
    'Março': 'March',
    'Abril': 'April',
    'Maio': 'May',
    'Junho': 'June',
    'Julho': 'July',
    'Agosto': 'August',
    'Setembro': 'September',
    'Outubro': 'October',
    'Novembro': 'November',
    'Dezembro': 'December'
}
```

```python
# replaces month names in portuguese with their english equivalents
for m_pt, m_en in months.items():
    df['Publish Date'] = df['Publish Date'].str.replace(m_pt, m_en)
    df['Publish Date'] = df['Publish Date'].str.replace(' de ', ' ')

# change type
df['Publish Date'] = pd.to_datetime(df['Publish Date'], format='%d %B %Y %H:%M')
df['Publish Date']

print(df.info())
```
## Criando colunas de Categoria e Subcategoria
Nas linhas da coluna Summary podemos encontrar Categoria e Subcategoria, além de outras informações úteis. Não conseguimos capturar estes dados usando Selenium pela forma como eles estão dispostos no HTML, não são elementos como `<a>`, `<strong>`, etc.

A biblioteca BeautifulSoup também não ajuda aqui porque seu retorno é vazio ao tentar capturar os dados. Desta forma precisamos manualmente extrair as informações que desejamos.

Para esta atividade uso o ***Pandas*** para buscar os valores desejados, extrair as informações e criar novas colunas para serem preenchidas com o que for encontrado.

```python
# where exists 'Categoria'
count_cat = df[df['Summary'].str.contains('Categoria')].index.tolist()
print(f'A palavra "Categoria" aparece nas linhas: {count_cat}')

# where exists 'Subategoria'
count_subcat = df[df['Summary'].str.contains('Subcategoria')].index.tolist()
print(f'A palavra "Categoria" aparece nas linhas: {count_subcat}')
```

Aqui crio as novas colunas utilizando expressões regulares para retornar caracteres válidos entre os textos 'Categoria:' e 'Subategoria:' e a quebra de linha. Logo após preencho as linhas nulas com o texto 'N/I' que significa 'não informado'.

```python
# extract data
df['Category'] = df['Summary'].str.extract('Categoria:\s*(.*)\n')
df['Subcategory'] = df['Summary'].str.extract('Subcategoria:\s*(.*)\n')

# fill null values
df[['Category','Subcategory']] = df[['Category','Subcategory']].fillna('N/I')
```

Para finalizar esta parte resolvi remover todo o texto após a primeira quebra de linha. Assim temos apenas o resumo do trabalho, evitando informações demais em nosso dataframe.

```python
# remove after line break
df['Summary'] = df['Summary'].str.split('\n').str[0]
```

## Criando colunas para Skills

Podemos observar que a coluna ***Skills*** retorna uma string com o nome das habilidades mas não as separa. Deste modo decidi criar colunas para cada habilidade descrita em que o valor será ***True*** para cada habilidade envolvida no trabalho e ***False*** para as demais.

```python
# Replace substring - exclude spaces
df['Skills'] = df['Skills'].replace(' ','', regex=True)
```

Após remover os espaços e criar as novas colunas observa-se que foi criada a colua ***+***. Vamos removê-la pois aparentemente não é relevante.

```python
# create dummy columns
df = pd.concat([df, df['Skills'].str.get_dummies(sep=',')], axis = 1)
if '+' in df.columns:
    df.drop('+', axis=1, inplace=True)
```

## Exportando dados para arquivo .CSV
Agora temos o dataframe organizado, pronto para ser consultado e produzir análises. Vamos exportar os dados.

```python
#create csv
df.to_csv('../workana_scrapp/data/data_t.csv', index=False)
```

## Concluindo
Neste ponto o projeto se divide em duas partes. 

Primeiro vamos filtrar os dados e disponibilizá-los em um bot no Telegram. Desta forma sempre que quiser poderei consultar rapidamente os trabalhos disponíveis na plataforma.

Ao finalizar o bot irei usar estatítcia para analisar os dados para tentar extrair o máximo de informações puder, como produzir gráficos, dashboards e etc.

- [O bot telegram](/docs/bot_telegram.md)
- [As análies](/docs/analysis.md)
- [As referências](/docs/references.md)

