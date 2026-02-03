def avaliar_vacinas(idade_meses, doses_aplicadas):
    pode_administrar = []
    nao_indicadas = []

    calendario = {
       "BCG": [
    {"mes": 0, "tipo": "Dose única", "max": 59},
],
       # 🔶 HEPATITE B – REGRA ESPECIAL (RN apenas)
doses_hepb = doses_aplicadas.get("Hepatite B", [])

if idade_meses == 0 and not doses_hepb:
    pode_administrar.append({
        "vacina": "Hepatite B",
        "dose": "Dose RN",
        "faltam": 0
    })


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
            {"mes": 15, "tipo": "D2"},
        ],

        "DTP": [
            {"mes": 15, "tipo": "R"},
            {"mes": 48, "tipo": "R"},
        ],

        "Hepatite A": [
    {"mes": 15, "tipo": "D1", "max": 59},
],

    }

    # 🔶 FEBRE AMARELA – REGRA ESPECIAL
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

    # 🔷 DEMAIS VACINAS
    for vacina, esquema in calendario.items():
        aplicadas = doses_aplicadas.get(vacina, [])

        for dose in esquema:
            mes_dose = dose["mes"]
            tipo = dose["tipo"]
            idade_max = dose.get("max")

            if idade_meses < mes_dose:
                continue

            if idade_max is not None and idade_meses > idade_max:
                nao_indicadas.append(f"{vacina} — fora da idade permitida")
                continue

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
