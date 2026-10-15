"""Microservizio magazzino: giacenze per prodotto, in memoria."""

from threading import Lock

from flask import Flask, jsonify, request


class Magazzino:
    """Archivio in memoria: i dati si azzerano a ogni riavvio."""

    def __init__(self) -> None:
        self._giacenze: dict[int, int] = {1: 25, 2: 40, 3: 8}
        self._lock = Lock()

    def tutte(self) -> list[dict]:
        return [{"prodottoId": pid, "quantita": q} for pid, q in sorted(self._giacenze.items())]

    def quantita(self, prodotto_id: int) -> int | None:
        return self._giacenze.get(prodotto_id)

    def movimento(self, prodotto_id: int, delta: int) -> int:
        with self._lock:
            attuale = self._giacenze.get(prodotto_id, 0)
            nuova = attuale + delta
            if nuova < 0:
                raise ValueError(f"giacenza insufficiente: disponibili {attuale}")
            self._giacenze[prodotto_id] = nuova
            return nuova


def create_app(magazzino: Magazzino | None = None) -> Flask:
    app = Flask(__name__)
    store = magazzino or Magazzino()

    @app.get("/health")
    def health():
        return jsonify(status="UP", service="magazzino-service")

    @app.get("/giacenze")
    def elenco():
        return jsonify(store.tutte())

    @app.get("/giacenze/<int:prodotto_id>")
    def dettaglio(prodotto_id: int):
        quantita = store.quantita(prodotto_id)
        if quantita is None:
            return jsonify(messaggio="prodotto non presente in magazzino"), 404
        return jsonify(prodottoId=prodotto_id, quantita=quantita)

    @app.post("/giacenze/<int:prodotto_id>/movimenti")
    def movimento(prodotto_id: int):
        body = request.get_json(silent=True) or {}
        delta = body.get("delta")
        if not isinstance(delta, int) or isinstance(delta, bool) or delta == 0:
            return jsonify(messaggio="delta deve essere un intero diverso da zero"), 400
        try:
            nuova = store.movimento(prodotto_id, delta)
        except ValueError as err:
            return jsonify(messaggio=str(err)), 409
        return jsonify(prodottoId=prodotto_id, quantita=nuova)

    return app
