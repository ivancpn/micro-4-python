# micro-4-python · magazzino-service

Microservizio **Python** con Flask che gestisce le giacenze per prodotto. Dati in memoria.

| | |
|---|---|
| Porta | `8084` (variabile `PORT`) |
| Health | `GET /health` |

## Requisiti

- Python 3.10+

## Comandi (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python main.py                 # avvio in debug
python -m unittest -v          # test
```

## API

| Metodo | Path | Descrizione |
|---|---|---|
| GET | `/giacenze` | elenco giacenze |
| GET | `/giacenze/{prodottoId}` | giacenza di un prodotto, 404 se assente |
| POST | `/giacenze/{prodottoId}/movimenti` | carico/scarico: `{"delta": 5}` oppure `{"delta": -2}` (409 se la giacenza va sotto zero) |
