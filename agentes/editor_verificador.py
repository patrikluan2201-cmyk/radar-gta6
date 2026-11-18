#!/usr/bin/env python3
"""Triagem editorial de manchetes. Não confirma fatos nem publica conteúdo."""
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

PASTA = Path("relatorios")
ENTRADA = PASTA / "noticias.json"
SINAIS = {
    "afirmação sobre lançamento": ["lanca amanha", "chega amanha", "estreia hoje", "ja lancou", "data de lancamento", "quando sera lancado"],
    "avaliação ou análise pós-lançamento": ["review", "analise do jogo", "metacritic", "mais bem avaliado"],
    "números e recordes exigem fonte": ["bilhao", "recorde", "maior lancamento", "receita", "mais vendido"],
    "mecânicas e funcionalidades não confirmadas": ["mecanismos", "pela primeira vez", "inteligencia artificial", "furacoes", "empatia"],
}
def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in texto if not unicodedata.combining(c))

def analisar(item, vistos):
    titulo = item.get("titulo", "")
    base = normalizar(titulo)
    base = re.sub(r"\s+-\s+[^-]+$", "", base).strip()
    base = re.sub(r"[^a-z0-9 ]", " ", base)
    chave = " ".join(base.split())
    motivos = []
    if chave in vistos:
        motivos.append("possível duplicata exata de título")
    vistos.add(chave)
    norm = normalizar(titulo)
    for motivo, termos in SINAIS.items():
        if any(t in norm for t in termos):
            motivos.append(motivo)
    if not item.get("link"):
        motivos.append("link ausente")
    if not item.get("fonte") or item.get("fonte") == "Fonte não identificada":
        motivos.append("fonte não identificada")
    return {
        "titulo": titulo,
        "fonte": item.get("fonte", ""),
        "data": item.get("data", ""),
        "link": item.get("link", ""),
        "prioridade": "ALTA" if motivos else "NORMAL",
        "alertas": motivos,
        "situacao": "NAO_VERIFICADA",
        "proxima_acao": "Ler a matéria original e confrontar afirmações com fontes primárias.",
    }

def main():
    if not ENTRADA.exists():
        raise SystemExit("Falta relatorios/noticias.json. Execute o Caçador primeiro.")
    dados = json.loads(ENTRADA.read_text(encoding="utf-8"))
    vistos = set()
    resultados = [analisar(item, vistos) for item in dados.get("noticias", [])]
    saida = {"gerado_em_utc": datetime.now(timezone.utc).isoformat(),
             "aviso": "Triagem automática por palavras-chave; nenhuma notícia foi verificada.",
             "itens": resultados}
    PASTA.mkdir(parents=True, exist_ok=True)
    (PASTA / "triagem.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    linhas = ["# Radar GTA 6 — Triagem editorial", "",
              "**Nenhuma notícia foi verificada ou aprovada automaticamente.**",
              "Os alertas são heurísticos e podem gerar falsos positivos ou deixar passar erros.", ""]
    for numero, item in enumerate(resultados, 1):
        linhas.extend([f"## {numero}. {item['titulo']}", "",
            f"- Prioridade de checagem: **{item['prioridade']}**",
            f"- Fonte indicada: {item['fonte']}",
            f"- Link: {item['link']}",
            f"- Alertas: {', '.join(item['alertas']) if item['alertas'] else 'nenhum alerta automático'}",
            "- Situação: NÃO VERIFICADA — requer revisão humana", ""])
    (PASTA / "triagem.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"Triagem concluída: {len(resultados)} manchetes, nenhuma aprovada automaticamente.")

if __name__ == "__main__":
    main()
