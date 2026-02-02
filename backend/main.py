from motor_decisao import avaliar_vacinas

pode, agendar, nao = avaliar_vacinas(
    anos=1,
    meses=4,
    doses_recebidas={
        "Pentavalente": 1,
        "VIP": 1
    },
    intervalo_ultima_dose=180
)

print("PODE ADMINISTRAR:", pode)
print("AGENDAR:", agendar)
print("NÃO INDICADA:", nao)
