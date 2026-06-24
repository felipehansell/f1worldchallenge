import json, urllib.request, urllib.parse, csv, io, os, datetime

SHEET_ID = "1ahdqArTj45LoNf2xq_BoyZ5Sz8sobToB-lKHpfJwqoE"

def fetch_sheet(name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(name)}"
    with urllib.request.urlopen(url) as r:
        return list(csv.reader(io.StringIO(r.read().decode('utf-8'))))

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {path}")

# POS / PILOTO / PTS / PEN
def parse_classificacao(sheet_name, div_id, div_nome, emoji):
    rows = fetch_sheet(sheet_name)
    pilotos = []
    for row in rows[1:]:
        if not row or not row[1].strip():
            continue
        try:
            pos = int(float(row[0])) if row[0].strip() else len(pilotos) + 1
        except:
            pos = len(pilotos) + 1
        nome = row[1].strip()
        try:
            pts = int(float(row[2])) if len(row) > 2 and row[2].strip() else 0
        except:
            pts = 0
        try:
            pen = int(float(row[3])) if len(row) > 3 and row[3].strip() else 0
        except:
            pen = 0
        pilotos.append({
            "posicao": pos,
            "nome": nome,
            "foto": f"imagens/pilotos/{nome.lower().replace(' ', '-')}.jpg",
            "pontos": pts,
            "penalizacoes": pen
        })
    return {"id": div_id, "nome": div_nome, "emoji": emoji, "pilotos": pilotos}

# POS / TEAMS / PTS / PEN
def parse_duplas(sheet_name):
    rows = fetch_sheet(sheet_name)
    duplas = []
    for row in rows[1:]:
        if not row or not row[1].strip():
            continue
        try:
            pos = int(float(row[0])) if row[0].strip() else len(duplas) + 1
        except:
            pos = len(duplas) + 1
        dupla = row[1].strip()
        try:
            pts = int(float(row[2])) if len(row) > 2 and row[2].strip() else 0
        except:
            pts = 0
        try:
            pen = int(float(row[3])) if len(row) > 3 and row[3].strip() else 0
        except:
            pen = 0
        duplas.append({"posicao": pos, "dupla": dupla, "pontos": pts, "penalizacoes": pen})
    return duplas

# POS / CONSTRUCTORS / PTS / PEN
def parse_construtores():
    rows = fetch_sheet("Construtores AeB")
    construtores = []
    for row in rows[1:]:
        if not row or not row[1].strip():
            continue
        try:
            pos = int(float(row[0])) if row[0].strip() else len(construtores) + 1
        except:
            pos = len(construtores) + 1
        nome = row[1].strip()
        try:
            pts = int(float(row[2])) if len(row) > 2 and row[2].strip() else 0
        except:
            pts = 0
        try:
            pen = int(float(row[3])) if len(row) > 3 and row[3].strip() else 0
        except:
            pen = 0
        construtores.append({"posicao": pos, "nome": nome, "pontos": pts, "penalizacoes": pen})
    return construtores

# PILOTO / DATA / INCIDENTE / PENALIDADE — agrupa por piloto
def parse_punicoes():
    rows = fetch_sheet("Punições")
    agrupado = {}
    ordem = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        piloto = row[0].strip()
        data   = row[1].strip() if len(row) > 1 else ""
        incidente = row[2].strip() if len(row) > 2 else ""
        penalidade = row[3].strip() if len(row) > 3 else ""
        if piloto not in agrupado:
            agrupado[piloto] = []
            ordem.append(piloto)
        if incidente:
            agrupado[piloto].append({
                "data": data,
                "incidente": incidente,
                "penalidade": penalidade
            })
    resultado = []
    for piloto in ordem:
        resultado.append({
            "piloto": piloto,
            "total_incidentes": len(agrupado[piloto]),
            "ocorrencias": agrupado[piloto]
        })
    return {
        "aviso": "A partir da temporada XXV, essa tabela é acumulativa e zerada apenas quando trocarmos para o próximo jogo: F126.",
        "email_recursos": "worldchallengeleague@gmail.com",
        "punicoes": resultado
    }

# CIRCUITO / P1 / P2 / ... / P14
def parse_corridas():
    rows = fetch_sheet("Corridas")
    corridas = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        circuito = row[0].strip()
        vencedores = []
        for cell in row[1:]:
            v = cell.strip()
            if v:
                vencedores.append(v)
        corridas.append({
            "circuito": circuito,
            "foto": f"imagens/circuitos/{circuito.lower().replace(' ', '-')}.jpg",
            "p1": vencedores[0] if len(vencedores) > 0 else "",
            "vencedores": vencedores
        })
    return {"corridas": corridas}

# POS / PILOTO / TITLES / VICTORIES / VIC-SPR / SECOND / THIRD / VIC-DIVB / PODIUMS / PPR / POLES / RACES / DNF / DNF%
def parse_historico():
    rows = fetch_sheet("Histórico")
    pilotos = []
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        def val(idx):
            try:
                return row[idx].strip() if idx < len(row) else ""
            except:
                return ""
        def ival(idx):
            try:
                v = row[idx].strip() if idx < len(row) else ""
                return int(float(v)) if v else 0
            except:
                return 0
        pilotos.append({
            "posicao":       val(0),
            "piloto":        val(1),
            "titulos":       ival(2),
            "vitorias":      ival(3),
            "vic_sprint":    ival(4),
            "segundos":      ival(5),
            "terceiros":     ival(6),
            "vic_div_b":     ival(7),
            "podiums":       ival(8),
            "ppr":           val(9),
            "poles":         ival(10),
            "corridas":      ival(11),
            "dnf":           ival(12),
            "dnf_pct":       val(13)
        })
    return {"historico": pilotos}

def main():
    print("Sincronizando...")

    div_a = parse_classificacao("Classificação A", "A", "Divisão A", "🥇")
    div_b = parse_classificacao("Classificação B", "B", "Divisão B", "🥈")
    div_c = parse_classificacao("Classificação C", "C", "Divisão C", "🥉")

    print(f"Div A: {len(div_a['pilotos'])} pilotos")
    print(f"Div B: {len(div_b['pilotos'])} pilotos")
    print(f"Div C: {len(div_c['pilotos'])} pilotos")

    temporada = {
        "liga": "F1 World Challenge",
        "temporada": 27,
        "jogo": "F1 25",
        "ultima_atualizacao": datetime.date.today().strftime("%d/%m/%Y"),
        "total_rodadas": 22,
        "divisoes": [div_a, div_b, div_c],
        "duplas_ab": parse_duplas("Duplas A e B"),
        "duplas_c":  parse_duplas("Duplas C"),
        "construtores": parse_construtores()
    }

    save_json("data/temporada.json", temporada)
    save_json("data/punicoes.json",  parse_punicoes())
    save_json("data/corridas.json",  parse_corridas())
    save_json("data/historico.json", parse_historico())
    print("Concluído!")

if __name__ == "__main__":
    main()
