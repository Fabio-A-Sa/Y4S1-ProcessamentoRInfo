# Data Processing

É o processo que inclui também o `Data Storage` e `Data Presentation`. Por motivos de documentação é importante a criação de um **Data Model** que garanta uma abstração dos documentos finais. Há alguns tipos:

### 1 - Relational Model

É o mais dominante e conhecido. É organizado em relações entre entidades. NoSQL proporciona nestes sistemas uma melhor escalabilidade e queries mais especializadas e flexíveis.

### 2 - Document Model

Os dados são organizados em instâncias / documentos com a mesma estrutura. Também conhecidos como document-oriented databases. As principais vantagens são flexibilidade no schema, melhor performance em termos locais, é mais próximo da realidade. <br>
O Relational Model é ainda melhor em relações N-N ou 1-N.

### 3 - Graph-based Model

Usado quando a aplicação é maioritariamente N-N. Há vértices (nós ou entidades) e arestas (que são as relações). É vantagem deste modelo não estar limitado a dados homogéneos e garantir um adequado tratamento de dados mesmo que tenham diferentes tipos.

### 4 - Triple-Store Model

Formado por tuplos com três itens: subject, predicate, object. Exemplo: (PRI, course, M.EIC). 