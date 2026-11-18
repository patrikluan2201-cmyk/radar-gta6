#!/usr/bin/env python3
"""Radar GTA 6: coleta manchetes para revisão humana, sem publicar notícias."""
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

QUERY = '("GTA VI" OR "GTA 6" OR "Grand Theft Auto VI")'
RSS_URL = "https://news.google.com/rss/search?" + urllib.parse.urlencode({
    "q": QUERY, "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419"
})
OUTPUT = Path(os.environ.get("RADAR_OUTPUT", "relatorios"))
LIMIT = 15

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(RSS_URL, headers={
        "User-Agent": "RadarGTA6-NewsMonitor/1.0 (personal news review)"
    })
    with urllib.request.urlopen(request, timeout=25) as response:
        xml_data = response.read(2_000_000)
    root = ET.fromstring(xml_data)
    entries = []
    seen = set()
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        source = item.find("source")
        source_name = (source.text or "").strip() if source is not None else "Fonte não identificada"
        date_raw = (item.findtext("pubDate") or "").strip()
        if not title or not link or link in seen:
            continue
        seen.add(link)
        try:
            published = parsedate_to_datetime(date_raw).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError):
            published = date_raw
        entries.append({
            "titulo": title,
            "fonte": source_name,
            "data": published,
            "link": link,
            "status": "PENDENTE_DE_VERIFICACAO",
        })
        if len(entries) >= LIMIT:
            break

    now = datetime.now(timezone.utc).isoformat()
    report = {"gerado_em_utc": now, "consulta": QUERY, "noticias": entries}
    (OUTPUT / "noticias.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Radar GTA 6 — Monitor de notícias", "",
        f"Coleta (UTC): {now}", "",
        "**Atenção:** títulos coletados automaticamente não são fatos verificados.",
        "Abra as fontes originais e confirme com fontes oficiais antes de publicar.", "",
    ]
    if not entries:
        lines.append("Nenhuma notícia encontrada nesta execução.")
    for i, entry in enumerate(entries, 1):
        lines.extend([
            f"## {i}. {entry['titulo']}", "",
            f"- Fonte indicada pelo agregador: {entry['fonte']}",
            f"- Data: {entry['data']}",
            f"- Link para conferir: {entry['link']}",
            "- Situação: aguardando verificação editorial", "",
        ])
    (OUTPUT / "revisao.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Coleta concluída: {len(entries)} títulos para revisão.")
    print(f"Relatórios disponíveis em: {OUTPUT.resolve()}")

if __name__ == "__main__":
    main()
