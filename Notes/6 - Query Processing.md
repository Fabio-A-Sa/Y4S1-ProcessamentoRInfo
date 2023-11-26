# Query Processing

Um dos principais desafios é, dada uma query, encontrar os resultados procurados. Para isso existem dois métodos principais:

- `Document-at-a-time`: calcula os scores de cada documento processando todos como uma lista, um documento de cada vez. No final os documentos são ordenados de acordo com o seu score;
- `Term-at-a-time`: acumula os scores dos documentos processando os termos na lista um de cada vez. No final faz-se também a ordenação segundo os scores acumulados em cada um deles;

Existem otimizações possíveis nestes processos, pois as funções de score são complexas e demoradas:

- Ler menos dados do index/query;
- Processar menos documentos;

## Otimizações

- Skip Pointers: 