def avaliar_vacinas(idade_meses, doses_aplicadas):
    pode_administrar = []
    nao_indicadas = []

    calendario = {
        "BCG": [
            {"mes": 0, "tipo": "Dose única", "max": 59},
        ],

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

        "Tetraviral (SCR + Varicela)": [
            {"mes": 15, "tipo": "D2"},
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

    # 🔶 TETRAVIRAL – RESGATE
    doses_tetra = doses_aplicadas.get("Tetraviral (SCR + Varicela)", [])
    if idade_meses >= 15 and not doses_tetra:
        pode_administrar.append({
            "vacina": "Tetraviral (SCR + Varicela)",
            "dose": "D2",
            "faltam": 0
        })

    bloquear_varicela = idade_meses >= 15 and not doses_tetra

    # 🔶 MENINGOCÓCICA ACWY
    doses_menc = doses_aplicadas.get("Meningocócica C", [])
    doses_acwy = doses_aplicadas.get("Meningocócica ACWY", [])
    tem_menc_d2 = len(doses_menc) >= 2

    if (
        idade_meses >= 12
        and idade_meses <= 59
        and tem_menc_d2
        and not doses_acwy
    ):
        pode_administrar.append({
            "vacina": "Meningocócica ACWY",
            "dose": "Dose única",
            "faltam": 0,
            "obs": "Respeitar intervalo mínimo de 60 dias após a 2ª dose da meningocócica C."
        })

    # 🔶 FEBRE AMARELA
    doses_fa = doses_aplicadas.get("Febre Amarela", [])
    if idade_meses >= 60:
        if not doses_fa:
            pode_administrar.append({
                "vacina": "Febre Amarela",
                "dose": "Dose única",
                "faltam": 0
            })
    else:
        esquema_fa = [
            {"mes": 9, "tipo": "D1"},
            {"mes": 48, "tipo": "R"},
        ]

        for dose in esquema_fa:
            if idade_meses < dose["mes"]:
                continue
            if dose["mes"] in doses_fa:
                continue

            futuras = [
                d for d in esquema_fa
                if d["mes"] > dose["mes"] and d["mes"] not in doses_fa
            ]

            pode_administrar.append({
                "vacina": "Febre Amarela",
                "dose": dose["tipo"],
                "faltam": len(futuras)
            })
            break

    # 🔶 HEPATITE B (RN)
    doses_hepb = doses_aplicadas.get("Hepatite B", [])
    if idade_meses == 0 and not doses_hepb:
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
            doses_penta = doses_aplicadas.get("Pentavalente", [])
            if len(doses_penta) < 3:
                continue

        if all(d["mes"] in aplicadas for d in esquema):
            continue

        for dose in esquema:
            mes_dose = dose["mes"]
            tipo = dose["tipo"]
            idade_max = dose.get("max")

            if idade_meses < mes_dose:
                continue

            if idade_max is not None and idade_meses > idade_max:
                nao_indicadas.append(f"{vacina} — fora da idade permitida")
                break

            if mes_dose in aplicadas:
                continue

            futuras = [
                d for d in esquema
                if d["mes"] > mes_dose and d["mes"] not in aplicadas
            ]

            pode_administrar.append({
                "vacina": vacina,
                "dose": tipo,
                "faltam": len(futuras)
            })
            break

    return pode_administrar, nao_indicadas
