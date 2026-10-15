import unittest

from magazzino.app import create_app


class MagazzinoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_app().test_client()

    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "UP")

    def test_elenco_giacenze(self):
        res = self.client.get("/giacenze")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()), 3)

    def test_prodotto_inesistente(self):
        self.assertEqual(self.client.get("/giacenze/999").status_code, 404)

    def test_carico_e_scarico(self):
        res = self.client.post("/giacenze/3/movimenti", json={"delta": 2})
        self.assertEqual(res.get_json()["quantita"], 10)
        res = self.client.post("/giacenze/3/movimenti", json={"delta": -10})
        self.assertEqual(res.get_json()["quantita"], 0)

    def test_scarico_oltre_giacenza(self):
        res = self.client.post("/giacenze/3/movimenti", json={"delta": -100})
        self.assertEqual(res.status_code, 409)

    def test_delta_non_valido(self):
        res = self.client.post("/giacenze/1/movimenti", json={"delta": "tanti"})
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
