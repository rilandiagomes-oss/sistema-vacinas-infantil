def avaliar_vacinas(idade_meses, doses_aplicadas):
    pode_administrar = []
    nao_indicadas = []

    calendario = {
        "BCG": [{"mes": 0, "tipo": "Dose única", "max": 59}],

        "Pentavalente": [
            {"mes": 2, "tipo": "D1"},
            {"mes": 4, "tipo": "D2"},
            {"mes": 6, "tipo": "D3"},
        ],

        "VIP": [
            {"mes": 2, "tipo": "D1"},
            {"mes": 4, "tipo": "D2"},
            {"mes": 6, "tipo": "D3"},
        ],

        "Rotavírus": [
            {"mes": 2, "tipo": "D1", "max": 7.9},
            {"mes": 4, "tipo": "D2", "max": 7.9},
        ],

        "Pneumocócica 10v": [
            {"mes": 2, "tipo": "D1"},
            {"mes": 4, "tipo": "D2"},
            {"mes": 12, "tipo": "R"},
        ],

        "Meningocócica C": [
            {"mes": 3, "tipo": "D1"},
            {"mes": 5, "tipo": "D2"},
            {"mes": 12, "tipo": "R"},
        ],

        "Tríplice Viral (SCR)": [
            {"mes": 12, "tipo": "D1"},
        ],

        "Varicela": [
            {"mes": 48, "tipo": "R", "max": 72},
        ],

        "DTP": [
            {"mes": 15, "tipo": "R"},
            {"mes": 48, "tipo": "R"},
        ],

        "Hepatite A": [
            {"mes": 15, "tipo": "D1", "max": 59},
        ],
    }

    # 🔶 TETRAVIRAL (REGRA CORRETA)
    doses_tetra = doses_aplicadas.get("Tetraviral (SCR + Varicela)", [])
    doses_scr = doses_aplicadas.get("Tríplice Viral (SCR)", [])

    if idade_meses >= 15 and not doses_tetra and len(doses_scr) >= 1:
        pode_administrar.append({
            "vacina": "Tetraviral (SCR + Varicela)",
            "dose": "Dose única",
            "faltam": 0
        })

    bloquear_varicela = idade_meses >= 15 and not doses_tetra

    # 🔶 ACWY
    doses_menc = doses_aplicadas.get("Meningocócica C", [])
    doses_acwy = doses_aplicadas.get("Meningocócica ACWY", [])

    if idade_meses >= 12 and idade_meses <= 59 and len(doses_menc) >= 2 and not doses_acwy:
        pode_administrar.append({
            "vacina": "Meningocócica ACWY",
            "dose": "Dose única",
            "faltam": 0,
            "obs": "Respeitar intervalo mínimo de 60 dias após a 2ª dose da meningocócica C."
        })

    # 🔶 FEBRE AMARELA
    doses_fa = doses_aplicadas.get("Febre Amarela", [])

    if not doses_fa:
        if idade_meses >= 9:
            faltam = 1 if idade_meses < 48 else 0
            pode_administrar.append({
                "vacina": "Febre Amarela",
                "dose": "D1",
                "faltam": faltam
            })

    elif len(doses_fa) == 1 and idade_meses >= 48:
        pode_administrar.append({
            "vacina": "Febre Amarela",
            "dose": "R",
            "faltam": 0
        })

    # 🔶 HEP B RN
    if idade_meses == 0 and not doses_aplicadas.get("Hepatite B"):
        pode_administrar.append({
            "vacina": "Hepatite B",
            "dose": "Dose RN",
            "faltam": 0
        })

    # 🔷 DEMAIS VACINAS
    for vacina, esquema in calendario.items():
        aplicadas = doses_aplicadas.get(vacina, [])

        if vacina == "Varicela" and bloquear_varicela:
            continue

        if vacina == "DTP":
            if len(doses_aplicadas.get("Pentavalente", [])) < 3:
                continue

        # evita erro rotavírus
        if all(d["mes"] in aplicadas for d in esquema):
            continue

        for dose in esquema:
            if idade_meses < dose["mes"]:
                continue

            if dose.get("max") and idade_meses > dose["max"]:
                nao_indicadas.append(f"{vacina} — fora da idade permitida")
                break

            if dose["mes"] in aplicadas:
                continue

            futuras = [d for d in esquema if d["mes"] > dose["mes"] and d["mes"] not in aplicadas]

            pode_administrar.append({
                "vacina": vacina,
                "dose": dose["tipo"],
                "faltam": len(futuras)
            })
            break

    return pode_administrar, nao_indicadas
