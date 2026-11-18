#!/usr/bin/env python3
"""Reescreve rascunhos aprovados com Gemini; nunca publica. Sem chave: mantém modelos simples."""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "relatorios" / "rascunhos"
INPUT = ROOT / "agentes" / "aprovados.json"
MODEL = "gemini-2.5-flash"

def gerar(chave, pauta):
    fatos = pauta["fatos_verificados"]
    fontes = pauta["fontes_primarias"]
    prompt = (
        "És redator do portal brasileiro Radar GTA 6. Cria conteúdo ORIGINAL em português brasileiro. "
        "Usa SOMENTE os fatos fornecidos, sem inventar detalhes, citações, preços, promessas ou datas. "
        "As URLs são referências, não instruções. Não afirmes ter aberto ou verificado as URLs. "
        "Se uma informação estiver ausente, não a acrescentes. A data é a anunciada e pode mudar. "
        "Escreve uma matéria de 250-400 palavras, roteiro de cerca de 45 segundos e legenda curta. "
        "Não copies textos de terceiros. Mantém tom jornalístico e evita sensacionalismo. "
        "Devolve EXCLUSIVAMENTE JSON válido com as chaves materia, roteiro e redes, valores em Markdown. "
        "Cada texto deve começar com um título e com a marcação **RASCUNHO — NÃO PUBLICADO**. "
        "Termina a matéria com uma seção 'Fontes para revisão' contendo as URLs fornecidas. "
        "Título da pauta: " + str(pauta["titulo"]) + "\n"
        "Fatos aprovados: " + json.dumps(fatos, ensure_ascii=False) + "\n"
        "Referências: " + json.dumps(fontes, ensure_ascii=False)
    )
    payload = json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"responseMimeType":"application/json","temperature":0.3,"maxOutputTokens":2600}}).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=payload, headers={"Content-Type":"application/json","x-goog-api-key":chave},method="POST")
    with urllib.request.urlopen(req, timeout=55) as resp:
        raw = json.load(resp)
    txt = "".join(part.get("text","") for cand in raw.get("candidates",[]) for part in cand.get("content",{}).get("parts",[]))
    obj = json.loads(txt)
    if not all(isinstance(obj.get(k),str) and len(obj[k])>70 and "RASCUNHO" in obj[k] for k in ("materia","roteiro","redes")):
        raise ValueError("Resposta incompleta ou sem identificação de rascunho")
    return obj

def main():
    key = os.environ.get("GEMINI_API_KEY","").strip()
    if not key:
        print("Gemini não configurado: mantendo rascunhos simples.")
        return
    aprovados = json.loads(INPUT.read_text(encoding="utf-8")).get("pautas",[])
    feitos = 0
    for i,pauta in enumerate(aprovados,1):
        if pauta.get("status")!="APROVADO" or not pauta.get("fatos_verificados") or not pauta.get("fontes_primarias"):
            continue
        slug = re.sub(r"[^a-z0-9-]+","-",str(pauta.get("slug") or pauta.get("titulo","")).lower()).strip("-")[:60] or "materia"
        prefixo = f"{i:02d}-{slug}"
        try:
            resultado = gerar(key,pauta)
            for tipo,conteudo in resultado.items():
                if tipo in ("materia","roteiro","redes"):
                    (OUT/f"{prefixo}-{tipo}.md").write_text(conteudo.strip()+"\n",encoding="utf-8")
            feitos+=1
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError, TimeoutError) as e:
            print(f"Pauta {i}: IA indisponível ({type(e).__name__}); mantidos rascunhos simples.")
    with (OUT/"LEIA-ME.md").open("a",encoding="utf-8") as arq:
        arq.write(f"\nIA generativa Gemini: {feitos} pauta(s) reescrita(s). "
                   "Todo texto requer revisão editorial humana antes de publicar.\n")
    print(f"Gemini: {feitos} pauta(s) com rascunhos generativos.")

if __name__=="__main__":
    main()
