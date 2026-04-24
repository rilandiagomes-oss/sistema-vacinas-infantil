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
    resultado_html = ""

    if request.method == "POST":
        idade = int(request.form.get("anos", 0)) * 12 + int(request.form.get("meses", 0))

        doses = {
            vacina: [int(m) for m in request.form.getlist(vacina)]
            for vacina in VACINAS_FORM
        }

        pode, nao = avaliar_vacinas(idade, doses)

        resultado_html += "<h3>🟢 Pode administrar</h3>"

        for item in pode:
            texto = f"<p><b>{item['vacina']}</b> — {item['dose']}</p>"
            if item.get("obs"):
                texto += f"<p style='color:orange'>⚠️ {item['obs']}</p>"
            resultado_html += texto

        if nao:
            resultado_html += "<h3>🔴 Não indicada</h3>"
            for v in nao:
                resultado_html += f"<p>{v}</p>"

    form = ""
    for vacina, meses in VACINAS_FORM.items():
        form += f"<p><b>{vacina}</b><br>"
        for m in meses:
            label = "ao nascer" if m == 0 else f"{m} meses"
            form += f'<input type="checkbox" name="{vacina}" value="{m}"> {label} '
        form += "</p>"

    return f"""
    <h2>Sistema de Vacinação</h2>
    <form method="post">
        Idade: <input name="anos"> anos <input name="meses"> meses
        {form}
        <button>Calcular</button>
    </form>
    {resultado_html}
    """

if __name__ == "__main__":
    app.run()
