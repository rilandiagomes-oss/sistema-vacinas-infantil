from flask import Flask, request
from motor_decisao import avaliar_vacinas

app = Flask(__name__)

VACINAS_FORM = {
    "BCG": [0],
    "Hepatite B": [0],
    "Pentavalente": [2, 4, 6],
    "VIP": [2, 4, 6],
    "Rotavírus": [2, 4],
    "Pneumocócica 10v": [2, 4, 12],
    "Meningocócica C": [3, 5, 12],
    "Tríplice Viral (SCR)": [12, 15],
    "Varicela": [15],
    "DTP": [15, 48],
    "Hepatite A": [15],
    "Febre Amarela": [9, 48],
}

@app.route("/", methods=["GET", "POST"])
def index():
    mostrar_resultado = False
    resultado_html = ""

    anos = 0
    meses = 0
    doses_marcadas = {}

    if request.method == "POST":
        mostrar_resultado = True

        anos = int(request.form.get("anos", 0))
        meses = int(request.form.get("meses", 0))
        idade_meses = anos * 12 + meses

        doses_marcadas = {
            vacina: request.form.getlist(vacina)
            for vacina in VACINAS_FORM
        }

        doses = {
            vacina: [int(m) for m in meses_lista]
            for vacina, meses_lista in doses_marcadas.items()
        }

        pode, nao = avaliar_vacinas(idade_meses, doses)

        # 🟢 Pode administrar
        resultado_html += "<div class='resultado pode'><h3>🟢 Pode administrar</h3>"

        if pode:
            for item in pode:
                vacina = item["vacina"]
                dose = item.get("dose", "")
                faltam = item.get("faltam", 0)

                dose_txt = "Reforço" if dose == "R" else dose

                if faltam == 0:
                    texto = f"<p><b>{vacina}</b> — {dose_txt}</p>"
                elif faltam == 1:
                    texto = (
                        f"<p><b>{vacina}</b> — {dose_txt}. "
                        "Após a administração de hoje, faltará uma dose.</p>"
                    )
                else:
                    texto = (
                        f"<p><b>{vacina}</b> — {dose_txt}. "
                        f"Após a administração de hoje, faltam {faltam} doses.</p>"
                    )

                resultado_html += texto
        else:
            resultado_html += "<p>Nenhuma vacina indicada.</p>"

        resultado_html += "</div>"

        # ⚠️ Alerta
        if len(pode) >= 5:
            resultado_html += (
                "<div class='alerta'>"
                "⚠️ Muitas vacinas indicadas nesta visita. Avaliar priorização clínica."
                "</div>"
            )

        # 🔴 Não indicadas
        if nao:
            resultado_html += "<div class='resultado nao'><h3>🔴 Não indicada</h3>"
            for v in nao:
                resultado_html += f"<p>{v}</p>"
            resultado_html += "</div>"

    # 🔽 Formulário de vacinas
    form_vacinas = ""
    for vacina, meses_vacina in VACINAS_FORM.items():
        form_vacinas += f"<div class='vacina'><b>{vacina}</b><br>"
        for m in meses_vacina:
            label = "ao nascer" if m == 0 else f"{m} meses"
            checked = ""
            if vacina in doses_marcadas and str(m) in doses_marcadas[vacina]:
                checked = "checked"
            form_vacinas += (
                f'<label><input type="checkbox" name="{vacina}" value="{m}" {checked}> {label}</label> '
            )
        form_vacinas += "</div>"

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sistema de TESTE NOVO SISTEMA</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f7fb;
                padding: 20px;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
            }}

            h2 {{
                text-align: center;
            }}

            .label-idade {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 8px;
                display: block;
            }}

            input[type="number"] {{
                font-size: 18px;
                padding: 10px;
                width: 100px;
                margin-right: 10px;
            }}

            .vacina {{
                background: #f8fafc;
                padding: 10px;
                margin-bottom: 8px;
                border-radius: 6px;
            }}

            button {{
                background: #0284c7;
                color: white;
                border: none;
                padding: 14px;
                border-radius: 8px;
                font-size: 18px;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            }}

            .secundario {{
                background: #64748b;
            }}

            .resultado {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
            }}

            .pode {{
                background: #ecfeff;
                border-left: 6px solid #06b6d4;
            }}

            .nao {{
                background: #fef2f2;
                border-left: 6px solid #ef4444;
            }}

            .alerta {{
                margin-top: 15px;
                background: #fff7ed;
                padding: 10px;
                border-left: 6px solid #f59e0b;
                border-radius: 6px;
                font-size: 14px;
            }}

            @media (max-width: 600px) {{
                input[type="number"] {{
                    width: 100%;
                    margin-bottom: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💉 Sistema de Apoio à Decisão – Imunização Infantil</h2>

            <form method="post">
                <label class="label-idade">Idade da criança:</label>
                <input type="number" name="anos" min="0" max="6" value="{anos}"> anos
                <input type="number" name="meses" min="0" max="11" value="{meses}"> meses

                <br><br>

                {form_vacinas}

                <button type="submit">Avaliar</button>
                <a href="/" style="text-decoration:none;">
                    <button type="button" class="secundario">Avaliar próximo caso</button>
                </a>
            </form>

            {"<hr>" + resultado_html if mostrar_resultado else ""}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
