import json
import urllib.request
import urllib.parse
import csv
import io
import os
import datetime

SHEET_ID = "1ahdqArTj45LoNf2xq_BoyZ5Sz8sobToB-lKHpfJwqoE"

def fetch_sheet(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"
    with urllib.request.urlopen(url) as r:
        return list(csv.reader(io.StringIO(r.read().decode('utf-8'))))

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {path}")

def parse_classificacao(sheet_name, div_id, div_nome, emoji):
    rows = fetch_sheet(sheet_name)
    corridas_row = rows[0]
    corridas = []
    col = 4
    while col < len(corridas_row):
        nome = corridas_row[col].strip()
        if nome:
            corridas.append({"col_pos": col, "col_pts": col + 1, "nome": nome})
        col += 2

    pilotos = []
    for row in rows[2:]:
        if not row or not row[1].strip():
            continue
        try:
            posicao = int(row[0]) if row[0].strip().lstrip('-').isdigit() else len(pilotos) + 1
        except:
            posicao = len(pilotos) + 1

        nome   = row[1].strip()
        pontos = row[2].strip() if len(row) > 2 else "0"
        pen    = row[3].strip() if len(row) > 3 else "0"

        try:
            pontos = int(float(pontos)) if pontos else 0
        except:
            pontos = 0
        try:
            pen = int(float(pen)) if pen else 0
        except:
            pen = 0

        resultados = []
        for c in corridas:
            pos_val = row[c["col_pos"]].strip() if c["col_pos"] < len(row) else ""
            pts_val = row[c["col_pts"]].strip() if c["col_pts"] < len(row) else "0"
            try:
                pts_int = int(float(pts_val)) if pts_val else 0
            except:
                pts_int = 0
            if pos_val in ("DNF", "NP", "DSQ", ""):
                pos_out = pos_val if pos_val else "NP"
            else:
                try:
                    pos_out = int(float(pos_val))
                except:
                    pos_out = pos_val
            resultados.append({"circuito": c["nome"], "posicao": pos_out, "pontos": pts_int})

        pilotos.append({
            "posicao": posicao,
            "nome": nome,
            "foto": f"imagens/pilotos/{nome.lower().replace(' ', '-')}.jpg",
            "pontos": pontos,
            "penalizacoes": pen,
            "resultados": resultados
        })

    return {"id": div_id, "nome": div_nome, "emoji": emoji, "pilotos": pilotos}

def parse_punicoes():
    rows = fetch_sheet("Punições")
    pilotos_resumo = {}
    detalhes = []
    modo = "resumo"

    for i, row in enumerate(rows):
        if i == 0:
            continue
        if not any(c.strip() for c in row):
            modo = "detalhe"
            continue
        piloto = row[0].strip() if row else ""
        if not piloto:
            continue
        if modo == "resumo":
            if piloto not in pilotos_resumo:
                pilotos_resumo[piloto] = {"ocorrencias": []}
        elif modo == "detalhe":
            data  = row[1].strip() if len(row) > 1 else ""
            descr = row[2].strip() if len(row) > 2 else ""
            if descr:
                detalhes.append({"piloto": piloto, "data": data, "descricao": descr})

    for d in detalhes:
        p = d["piloto"]
        if p not in pilotos_resumo:
            pilotos_resumo[p] = {"ocorrencias": []}
        pilotos_resumo[p]["ocorrencias"].append({"data": d["data"], "descricao": d["descricao"]})

    resultado = []
    for nome, dados in sorted(pilotos_resumo.items()):
        resultado.append({"piloto": nome, "ocorrencias": dados["ocorrencias"]})

    return {
        "aviso": "A partir da temporada XXV, essa tabela é acumulativa e zerada apenas quando trocarmos para o próximo jogo: F126.",
        "email_recursos": "worldchallengeleague@gmail.com",
        "punicoes": resultado
    }

def parse_corridas():
    rows = fetch_sheet("Corridas")
    circuitos = []
    for row in rows:
        if not row or not row[0].strip():
            continue
        nome = row[0].strip()
        contagem = {}
        for cell in row[1:]:
            cell = cell.strip()
            if not cell or ' -' not in cell:
                continue
            partes = cell.rsplit(' -', 1)
            piloto = partes[0].strip()
            try:
                n = int(partes[1].strip())
            except:
                n = 1
            contagem[piloto] = max(contagem.get(piloto, 0), n)
        maior_vencedor = max(contagem, key=contagem.get) if contagem else ""
        maior_vitorias = contagem.get(maior_vencedor, 0)
        circuitos.append({
            "id": nome.lower().replace(" ", "-"),
            "nome": nome,
            "foto": f"imagens/circuitos/{nome.lower().replace(' ', '-')}.jpg",
            "maior_vencedor": maior_vencedor,
            "vitorias_maior_vencedor": maior_vitorias
        })
    return {"circuitos": circuitos}

def parse_historico():
    rows = fetch_sheet("Histórico")
    pilotos = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        if not row or not row[0].strip():
            continue
        def val(idx, default=0):
            try:
                v = row[idx].strip() if idx < len(row) else ""
                return int(float(v)) if v else default
            except:
                return default
        pilotos.append({
            "posicao": row[0].strip(),
            "piloto":  row[1].strip() if len(row) > 1 else "",
            "titulos": val(2), "vitorias": val(3), "vitorias_sprint": val(4),
            "segundos": val(5), "terceiros": val(6), "podiums": val(7), "ppr": val(8)
        })
    return {"historico": pilotos}

def parse_duplas():
    rows = fetch_sheet("Duplas A e B")
    duplas = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        if not row or not row[0].strip():
            continue
        try:
            pos = int(row[0].strip())
        except:
            pos = i
        dupla  = row[1].strip() if len(row) > 1 else ""
        try:
            pontos = int(float(row[2].strip())) if len(row) > 2 and row[2].strip() else 0
        except:
            pontos = 0
        if dupla:
            duplas.append({"posicao": pos, "dupla": dupla, "pontos": pontos})
    return duplas

def main():
    print("Sincronizando dados do Google Sheets...")
    div_a = parse_classificacao("Classificação A", "A", "Divisão A", "🥇")
    div_b = parse_classificacao("Classificação B", "B", "Divisão B", "🥈")

    temporada = {
        "liga": "F1 World Challenge",
        "temporada": 27,
        "jogo": "F1 25",
        "ultima_atualizacao": datetime.date.today().strftime("%d/%m/%Y"),
        "ultima_corrida": div_a["pilotos"][0]["resultados"][-1]["circuito"] if div_a["pilotos"] else "",
        "proxima_corrida": "",
        "rodada_atual": len(div_a["pilotos"][0]["resultados"]) if div_a["pilotos"] else 0,
        "total_rodadas": 22,
        "divisoes": [div_a, div_b],
        "duplas": parse_duplas()
    }

    save_json("data/temporada.json", temporada)
    save_json("data/punicoes.json",  parse_punicoes())
    save_json("data/circuitos.json", parse_corridas())
    save_json("data/historico.json", parse_historico())
    print("Sincronização concluída!")

if __name__ == "__main__":
    main()
