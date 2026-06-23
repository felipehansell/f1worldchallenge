# F1 World Challenge — Site Oficial

## Estrutura de arquivos

```
f1wc/
├── index.html              ← site principal (não editar)
├── data/
│   ├── temporada.json      ← atualizar semanalmente após cada corrida
│   ├── punicoes.json       ← atualizar quando houver punições
│   ├── circuitos.json      ← atualizar após cada corrida (histórico)
│   └── historico.json      ← atualizar ao fim de cada temporada
└── imagens/
    ├── logo.png            ← logo da liga (subir uma vez)
    ├── pilotos/            ← fotos dos pilotos (ex: leo-costa.jpg)
    ├── circuitos/          ← fotos dos circuitos (ex: monaco.jpg)
    └── equipes/            ← logos das equipes (opcional)
```

---

## Como atualizar após cada corrida

### 1. Abra o arquivo `data/temporada.json` no GitHub

Clique no arquivo → botão de lápis (editar) no canto superior direito.

### 2. Atualize os campos principais

```json
"ultima_atualizacao": "29/06/2025",
"ultima_corrida": "México",
"proxima_corrida": "Brasil",
"rodada_atual": 11,
```

### 3. Atualize pontos e posições de cada piloto

Para cada piloto na divisão, atualize `pontos`, `posicao` e adicione o resultado da nova corrida em `resultados`:

```json
{
  "circuito": "Mexico",
  "posicao": 1,
  "pontos": 25
}
```

Posições especiais: `"DNF"` (não terminou), `"NP"` (não participou), `"DSQ"` (desqualificado).

### 4. Atualize o calendário

Mude o status da corrida de `"proxima"` para `"realizada"` e adicione o vencedor:

```json
{ "rodada": 11, "circuito": "Mexico", "status": "realizada", "vencedor": "Leo Costa" }
```

Mude a próxima corrida de `"futura"` para `"proxima"`.

### 5. Salve

Clique em **Commit changes** → **Commit directly to main** → **Commit changes**.

O site atualiza automaticamente em ~1 minuto.

---

## Como adicionar imagens

Suba as imagens na pasta correta dentro do GitHub:
- Fotos de pilotos → `imagens/pilotos/nome-do-piloto.jpg`
- Fotos de circuitos → `imagens/circuitos/nome-do-circuito.jpg`

No JSON, referencie assim:
```json
"foto": "imagens/pilotos/leo-costa.jpg"
```

Formatos aceitos: `.jpg`, `.png`, `.webp`  
Tamanho recomendado: fotos de piloto 400×400px, circuitos 800×450px.

---

## Como adicionar uma punição

No arquivo `data/punicoes.json`, encontre o piloto e adicione uma ocorrência:

```json
{
  "corrida": "Mexico",
  "temporada": 27,
  "tipo": "Colisão",
  "descricao": "Colisão com piloto adversário na volta 5.",
  "penalidade": "Drive through",
  "pontos": -10
}
```

Se o piloto ainda não existe na lista, adicione um bloco novo:

```json
{
  "piloto": "Nome do Piloto",
  "ocorrencias": [ ... ]
}
```
