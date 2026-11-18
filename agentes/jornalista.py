#!/usr/bin/env python3
"""Gera rascunhos editoriais de conteúdo aprovado. Sem IA externa e sem publicação."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "agentes" / "aprovados.json"
OUT = ROOT / "relatorios" / "rascunhos"

def safe(s):
    return re.sub(r"[^a-z0-9-]+", "-", s.lower().strip()).strip("-")[:60] or "materia"

def main():
    dados = json.loads(INPUT.read_text(encoding="utf-8"))
    itens = dados.get("pautas", [])
    OUT.mkdir(parents=True, exist_ok=True)
    aprovados = 0
    for n, item in enumerate(itens, 1):
        if item.get("status") != "APROVADO" or not item.get("fatos_verificados") or not item.get("fontes_primarias"):
            continue
        titulo = item["titulo"].strip()
        fatos = [str(x).strip() for x in item["fatos_verificados"] if str(x).strip()]
        fontes = [str(x).strip() for x in item["fontes_primarias"] if str(x).strip()]
        if not titulo or not fatos or not fontes or any(not x.startswith(("https://", "http://")) for x in fontes):
            continue
        nome = f"{n:02d}-{safe(item.get('slug') or titulo)}"
        corpo = "\n\n".join(fatos)
        refs = "\n".join(f"- {url}" for url in fontes)
        materia = (f"# {titulo}\n\n**RASCUNHO — NÃO PUBLICADO**\n\n"
                   f"## O que sabemos\n\n{corpo}\n\n"
                   f"## Fontes para conferência final\n\n{refs}\n\n"
                   "## Revisão pendente\n\nConferir contexto, atualidade, precisão, autoria, direitos de imagem e título antes de publicar.\n")
        roteiro = (f"# Roteiro curto — {titulo}\n\n**RASCUNHO — NÃO PUBLICADO**\n\n"
                   f"**Abertura:** Olha essa atualização sobre GTA VI!\n\n"
                   f"**Informações verificadas:** {(' '.join(fatos))[:650]}\n\n"
                   "**Encerramento:** Acompanhe o Radar GTA 6 para mais informações verificadas.\n\n"
                   "Ajustar a duração na leitura e confirmar todos os fatos antes de gravar.\n")
        social = (f"# Redes sociais — {titulo}\n\n**RASCUNHO — NÃO PUBLICADO**\n\n"
                  f"{titulo}\n\nConfira os detalhes e as fontes no Radar GTA 6.\n\n"
                  "#GTA6 #GTAVI #RadarGTA6 #Games\n")
        for sufixo, texto in [("materia", materia), ("roteiro", roteiro), ("redes", social)]:
            (OUT / f"{nome}-{sufixo}.md").write_text(texto, encoding="utf-8")
        aprovados += 1
    (OUT / "LEIA-ME.md").write_text(
        f"# Jornalista — {datetime.now(timezone.utc).isoformat()}\n\n"
        f"Pautas aprovadas processadas: {aprovados}.\n\n"
        "Sem IA generativa nesta versão: os textos são modelos organizados a partir dos fatos fornecidos. "
        "Nenhum conteúdo foi publicado.\n", encoding="utf-8")
    print(f"Jornalista: {aprovados} pauta(s) aprovada(s), rascunhos em {OUT}.")

if __name__ == "__main__":
    main()
