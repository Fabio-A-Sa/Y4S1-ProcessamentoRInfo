# Entity Oriented Search

## Entities

São usadas bases de conhecimento (*Knowledge Base*, KB), com factos acerca de entidades específicas para tornar a experiência de pesquisa melhor para os utilizadores. Pessoas, organizações, produtos, localizações e eventos são exemplos de entidades. Cada entidade tem:

- `Unique Identifier`: com relações de 1-1 entre entidades e objectos;
- `Name`: podem não ser únicos, e cada entidade pode ser conhecida por vários nomes;
- `Types`: agrupam entidades com características semelhantes;
- `Attributes`: caracterizam as features de cada entidade e têm sempre valores literais;
- `Relationships`: descreve como as entidades são associadas a outras, podem ser vistas como tipos de linkagem entre entidades;

`Resource Description Framework` (RDF) é o standard para descrever estas entidades. As entidades podem ser vistas como nós num grafo, com as relações a serem arestas.

Os utilizadores articulam as suas necessidades de informação através de cinco tipos diferentes:

- `Keyword queries`: free-text queries, são simples de formular mas imprecisas;
- `Structured queries`: com SQL, por exemplo, são precisas;
- `Keyword++ queries`: quando as keywords são complementadas com elementos estruturais, como "retrieval site:fe.up.pt" por exemplo;
- `Natural language queries`;
- `Zero queries`: em sistemas proativos, onde já estimam e prevêm as necessidades de informação do utilizador;

Os dados podem ser agrupados em três fases:

- `Unstructured data`: em vastas quantidades e em vários formatos;
- `Semi-structured data`: não tem uma estrutura rígida, mas existem tags ou alguma marca para separar elementos textuais de elementos semânticos, tal como acontece no HTML;
- `Structured data`: com um schema fixo e tabular, como nas bases de dados relacionais. O schema define como os dados são organizados e as duas restrições para manter a coerência e consistência.

## Data Sources

