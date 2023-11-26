# Query Processing

Um dos principais desafios é, dada uma query, encontrar os resultados procurados. Para isso existem dois métodos principais:

- `Document-at-a-time`: calcula os scores de cada documento processando todos como uma lista, um documento de cada vez. No final os documentos são ordenados de acordo com o seu score;
- `Term-at-a-time`: acumula os scores dos documentos processando os termos na lista um de cada vez. No final faz-se também a ordenação segundo os scores acumulados em cada um deles;

Existem otimizações possíveis nestes processos, pois as funções de score são complexas e demoradas:

- Ler menos dados do index/query;
- Processar menos documentos;

## Otimizações

### Skip Pointers

Usados para aumentar a rapidez do scan de `inverted indexes`.

### Conjunctive Processing

Apenas retorna documentos que contêm todos os termos da query. Este é o default das search engines e o default das expectativas dos utilizadores comuns. Este processo resulta melhor quando um dos termos da query é raro, ou seja, a maior parte da lista invertida dos outros termos pode ser avançada.

- Pode ser implementada com processos document-at-a-time e term-at-a-time;
- Em pequenas queries, há melhoramento em termos de eficiência e eficácia;
- Grandes queries não são boas candidatas porque a probabilidade de termos vários documentos com todos os termos diminui;

### Outras

- Ignorar as palavras com maior frequência nas listas no term-at-a-time;
- Ignorar os documentos no final da lista no document-at-a-time, quando os documentos começam a ser ordenados;
- Cache dos resultados das queries mais populares e comuns;

## Relevance Feedback

Exact match não é a única forma de obter resultados relevantes em search systems, porque existem sinónimos, imagens, e outras características da linguagem natural.

Nesse caso, o sistema pode retornar um conjunto inicial de resultados, pedir feedback ao utilizador e depois sim refinar o seguinte conjunto. Pode ajudar também o utilizador a refinar a sua query para aquela determinada search engine.

### Rocchio Algorithm

Maximiza a diferença entre vectores que representam documentos relevantes e documentos não relevantes. Considerando a informação relevante, este algoritmo define uma query modificada, pesada e combinada entre a query inicial e o centroide dos documentos marcados como relevantes pelo utilizador.

- Pode aumentar a precisão e o recall;
- É mais útil para aumentar o recall, pois é um comportamento global;
- O feedback positivo é mais importante que o negativo para afinar a query;

No entanto também há algumas limitações:

- Não aceita erros de escrita, documentos noutra lingua;
- Os utilizadores podem estar relutantes em dar feedback;

Há hipótese de fazer um `pseudo relevance feedback`, ou seja, sem interação com os utilizadores acabar por admitir que os primeiros K resultados do primeiro conjunto são relevantes e usar esses para afinar a query. Podemos também usar `implicit relevance feedback`, onde há medição do feedback de forma passiva, através de cliques ou links. É sempre melhor do que o método anterior já que há interação, ainda que pouca, do utilizador para o julgamento.

Através de `query expansion` o utilizador opta por dar queries ou termos alternativos, como sinónimos. 

## Search