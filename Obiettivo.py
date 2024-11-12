from datetime import datetime

def giorni_trascorsi():
    data_inizio = datetime(2024, 3, 1, 12, 0)
    data_attuale = datetime.now()
    differenza = data_attuale - data_inizio
    return differenza.total_seconds() / (24 * 60 * 60)

print(f'Il numero di giorni trascorsi dal 01/03/2024 alle ore 12:00 è {giorni_trascorsi()}, che moltiplicati per 10€ danno {giorni_trascorsi() * 10}€')