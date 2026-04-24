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
    "Meningocócica ACWY": [12],
    "Tríplice Viral (SCR)": [12],
    "Tetraviral (SCR + Varicela)": [15],
    "Varicela": [48],
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

        resultado_html += "<div class='resultado pode'><h3>🟢 Pode administrar</h3>"

        if pode:
            for item in pode:
                vacina = item["vacina"]
                dose = item.get("dose", "")
                faltam = item.get("faltam", 0)
                obs = item.get("obs", "")

                dose_txt = "Reforço" if dose == "R" else dose

                if faltam == 0:
                    texto = f"<p><b>{vacina}</b> — {dose_txt}</p>"
                elif faltam == 1:
                    texto = f"<p><b>{vacina}</b> — {dose_txt}. Após a administração de hoje, faltará uma dose.</p>"
                else:
                    texto = f"<p><b>{vacina}</b> — {dose_txt}. Após a administração de hoje, faltam {faltam} doses.</p>"

                if obs:
                    texto += f"<p style='color:#b45309; font-size:14px;'>⚠️ {obs}</p>"

                resultado_html += texto
        else:
            resultado_html += "<p>Nenhuma vacina indicada.</p>"

        resultado_html += "</div>"

        if nao:
            resultado_html += "<div class='resultado nao'><h3>🔴 Não indicada</h3>"
            for v in nao:
                resultado_html += f"<p>{v}</p>"
            resultado_html += "</div>"

    form_vacinas = ""
    for vacina, meses_vacina in VACINAS_FORM.items():
        form_vacinas += f"<div class='vacina'><b>{vacina}</b><br>"
        for m in meses_vacina:
            label = "ao nascer" if m == 0 else f"{m} meses"
            form_vacinas += f'<label><input type="checkbox" name="{vacina}" value="{m}"> {label}</label> '
        form_vacinas += "</div>"

    return f"""
    <html>
    <body>
        <h2>💉 Sistema de Imunização Infantil</h2>
        <form method="post">
            <input type="number" name="anos" placeholder="anos">
            <input type="number" name="meses" placeholder="meses">
            <br><br>
            {form_vacinas}
            <button type="submit">Avaliar</button>
        </form>
        {"<hr>" + resultado_html if mostrar_resultado else ""}
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
