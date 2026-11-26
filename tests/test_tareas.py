import unittest

from tareas import agregar, filtrar_por_prioridad, pendientes


class TestTareas(unittest.TestCase):
    def test_agregar(self):
        tareas = []
        self.assertEqual(agregar(tareas, "Leer")["id"], 1)

    def test_titulo_vacio(self):
        with self.assertRaises(ValueError):
            agregar([], " ")

    def test_prioridad_por_defecto_es_media(self):
        tarea = agregar([], "Leer")
        self.assertEqual(tarea["prioridad"], "media")

    def test_prioridad_valida(self):
        tareas = []
        for prioridad in ("alta", "media", "baja"):
            self.assertEqual(agregar(tareas, "x", prioridad)["prioridad"], prioridad)

    def test_prioridad_normaliza_mayusculas_y_espacios(self):
        self.assertEqual(agregar([], "x", "  ALTA ")["prioridad"], "alta")

    def test_prioridad_invalida(self):
        with self.assertRaises(ValueError):
            agregar([], "x", "urgente")

    def test_prioridad_no_texto(self):
        with self.assertRaises(ValueError):
            agregar([], "x", None)

    def test_filtrar_por_prioridad(self):
        tareas = []
        agregar(tareas, "A", "alta")
        agregar(tareas, "B", "baja")
        agregar(tareas, "C")
        self.assertEqual([t["titulo"] for t in filtrar_por_prioridad(tareas, "alta")], ["A"])
        self.assertEqual([t["titulo"] for t in filtrar_por_prioridad(tareas, "media")], ["C"])
        self.assertEqual(filtrar_por_prioridad(tareas, "baja")[0]["titulo"], "B")

    def test_filtrar_prioridad_invalida(self):
        with self.assertRaises(ValueError):
            filtrar_por_prioridad([], "urgente")

    def test_regresion_contrato_antiguo(self):
        tareas = []
        tarea = agregar(tareas, "  Leer  ")
        self.assertEqual(tarea["titulo"], "Leer")
        self.assertEqual(tarea["id"], 1)
        self.assertEqual(len(pendientes(tareas)), 1)
        pendientes(tareas).clear()
        self.assertEqual(len(tareas), 1)


if __name__ == "__main__":
    unittest.main()
