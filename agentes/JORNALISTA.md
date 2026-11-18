# Agente 3 — Jornalista

O Jornalista cria **rascunhos** de matéria, roteiro e legenda com base exclusivamente em pautas marcadas como `APROVADO` em `agentes/aprovados.json`.

## Segurança editorial
- As notícias recolhidas pelo Caçador e sinalizadas pelo Editor **não são automaticamente aprovadas**.
- O arquivo de aprovados começa vazio. Com ele vazio, o Jornalista gera apenas `LEIA-ME.md`.
- Uma pauta deve conter `titulo`, `slug`, `status: "APROVADO"`, `fatos_verificados` (lista de textos) e `fontes_primarias` (lista de URLs).
- O script não visita os links nem verifica fatos sozinho. Cabe ao editor humano verificar cada afirmação e confirmar que as fontes realmente a sustentam.
- Os rascunhos são gerados em `relatorios/rascunhos/` e entregues como artefatos do GitHub Actions.
- **Nenhuma matéria é publicada no site e nenhum vídeo é enviado às redes sociais.**

## Exemplo de pauta (substituir por fatos realmente conferidos)
```json
{
  "pautas": [
    {
      "titulo": "Título confirmado",
      "slug": "titulo-confirmado",
      "status": "APROVADO",
      "fatos_verificados": ["Informação conferida na fonte original."],
      "fontes_primarias": ["https://exemplo.com/fonte-original"]
    }
  ]
}
```

## Limitação
Esta versão é **gratuita e sem modelo de IA**: usa modelos de texto, não escreve uma reportagem criativa ou verifica notícias automaticamente. A integração com um modelo de IA poderá ser acrescentada depois, com aprovação editorial e controlo de custos.
