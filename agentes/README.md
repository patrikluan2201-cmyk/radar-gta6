# Agentes do Radar GTA 6

## Agente 1 — Caçador de Notícias

Este agente pesquisa manchetes públicas relacionadas a GTA VI usando um feed RSS do Google Notícias. Ele **não gera artigos, não verifica a veracidade das manchetes e não publica nada no site**.

### Execução automática
O GitHub Actions tenta executar diariamente às **12:15 UTC (09:15 em Brasília)**. A execução agendada pode sofrer atrasos e depende das configurações do GitHub Actions no repositório.

### Executar manualmente
No GitHub, abra **Actions** → **Radar GTA 6 - Cacador de Noticias** → **Run workflow**. Ao terminar, abra a execução e baixe o artefato **radar-gta6-noticias**.

O arquivo `revisao.md` contém uma lista de links para revisão editorial. O `noticias.json` contém os dados estruturados.

### Executar no computador
```bash
python agentes/cacador_noticias.py
```

Não requer bibliotecas externas nem chave de API. Depende de acesso à internet e da disponibilidade do RSS. Em caso de erro de rede, a execução falhará sem publicar conteúdo.

### Próximas etapas
1. Verificação editorial das fontes e distinção entre notícias oficiais, rumores e opiniões.
2. Geração de rascunhos originais de artigos e roteiros, com aprovação humana.
3. Produção de vídeo com FFmpeg.
4. Publicação no site após aprovação.

Não reutilize imagens, vídeos ou textos protegidos sem autorização. Não trate notícias agregadas como confirmações oficiais.
