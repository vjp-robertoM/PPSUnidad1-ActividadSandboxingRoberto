# tests/test_lavadero_custom.py

import unittest
from lavadero import Lavadero

class LavaderoTests(unittest.TestCase):
    """
    Pruebas unitarias para la clase Lavadero.
    Se incluyen:
    - Validaciones de reglas de negocio (caja negra)
    - Comprobación del flujo de fases y cálculo de ingresos (caja blanca)
    """

    def setUp(self):
        """Se crea un lavadero limpio antes de cada test."""
        self.lavadero = Lavadero()

    # =========================
    #  Caja negra
    # =========================

    def test_estado_inicial(self):
        """Verifica que el lavadero comienza inactivo, sin ingresos y no ocupado."""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.ocupado)
        self.assertEqual(self.lavadero.ingresos, 0.0)

    def test_no_iniciar_lavado_ocupado(self):
        """No se puede iniciar un lavado si el lavadero ya está ocupado."""
        self.lavadero.hacerLavado(prelavado_a_mano=False, secado_a_mano=False, encerado=False)
        with self.assertRaises(RuntimeError):
            self.lavadero.hacerLavado(prelavado_a_mano=True, secado_a_mano=True, encerado=True)

    def test_error_encerado_sin_secado(self):
        """Intentar encerar sin secado a mano lanza ValueError."""
        with self.assertRaises(ValueError):
            self.lavadero.hacerLavado(prelavado_a_mano=False, secado_a_mano=False, encerado=True)

    def test_ingresos_basicos(self):
        """Comprobación del precio base sin extras: 5.00€"""
        self.lavadero.hacerLavado(False, False, False)
        self.lavadero.avanzarFase()  # Cobro
        self.assertAlmostEqual(self.lavadero.ingresos, 5.00, places=2)

    def test_ingresos_con_todos_extras(self):
        """Lavado con prelavado, secado a mano y encerado: 8.70€"""
        self.lavadero.hacerLavado(True, True, True)
        self.lavadero.avanzarFase()  # Cobro
        self.assertAlmostEqual(self.lavadero.ingresos, 8.70, places=2)

    def test_ingresos_solo_prelavado(self):
        """Lavado solo con prelavado: 6.50€"""
        self.lavadero.hacerLavado(True, False, False)
        self.lavadero.avanzarFase()  # Cobro
        self.assertAlmostEqual(self.lavadero.ingresos, 6.50, places=2)

    # =========================
    # Caja blanca
    # =========================

    def test_recorrido_completo_sin_extras(self):
        """Verifica que se recorren todas las fases correctamente sin extras."""
        self.lavadero.hacerLavado(False, False, False)
        fases = [self.lavadero.fase]
        pasos = 0
        while self.lavadero.ocupado and pasos < 15:
            self.lavadero.avanzarFase()
            fases.append(self.lavadero.fase)
            pasos += 1

        self.assertFalse(self.lavadero.ocupado)
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertIn(Lavadero.FASE_COBRANDO, fases)

    def test_recorrido_completo_con_extras(self):
        """Verifica fases completas con prelavado, secado a mano y encerado."""
        self.lavadero.hacerLavado(True, True, True)
        fases = [self.lavadero.fase]
        pasos = 0
        while self.lavadero.ocupado and pasos < 15:
            self.lavadero.avanzarFase()
            fases.append(self.lavadero.fase)
            pasos += 1

        self.assertFalse(self.lavadero.ocupado)
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertIn(Lavadero.FASE_PRELAVADO_MANO, fases)
        self.assertIn(Lavadero.FASE_RODILLOS, fases)
        self.assertIn(Lavadero.FASE_COBRANDO, fases)

    def test_avanzar_fase_sin_lavado(self):
        """Si no hay lavado activo, avanzarFase no cambia nada."""
        fase_inicial = self.lavadero.fase
        ingresos_iniciales = self.lavadero.ingresos
        self.lavadero.avanzarFase()
        self.assertEqual(self.lavadero.fase, fase_inicial)
        self.assertEqual(self.lavadero.ingresos, ingresos_iniciales)

    def test_resetear_lavadero(self):
        """Comprobación de que terminar() reinicia el estado y los extras."""
        self.lavadero.hacerLavado(True, True, True)
        self.lavadero.terminar()
        self.assertFalse(self.lavadero.ocupado)
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertFalse(self.lavadero.secado_a_mano)
        self.assertFalse(self.lavadero.encerado)

if __name__ == "__main__":
    unittest.main()
