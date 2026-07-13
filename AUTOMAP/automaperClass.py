"""
automaper.py

Utilities for loading, visualizing and managing
photonic chip layouts.
"""

import pandas as pd
from pprint import pprint


class ChipManager:
    """
    Gestor de chips fotónicos.
    """
    
    def __init__(self, excel_file=None):
        self.excel_file = excel_file
        self.chip = None
        self.measurement_plan = None
        
        if excel_file:
            self.load_chip(excel_file)
    
    def load_chip(self, excel_file):
        """
        Carga un archivo Excel y guarda la información del chip
        junto con el plan de medida.
        """
        self.excel_file = excel_file
        
        metadata_df = pd.read_excel(excel_file, sheet_name="Metadata")
        devices_df = pd.read_excel(excel_file, sheet_name="Devices")
        ports_df = pd.read_excel(excel_file, sheet_name="Ports")
        measurements_df = pd.read_excel(excel_file, sheet_name="Measurements")
        
        self.chip = self._build_chip(
            metadata_df,
            devices_df,
            ports_df
        )
        
        self.measurement_plan = self._build_measurement_plan(
            measurements_df
        )
    
    def _build_chip(self, metadata_df, devices_df, ports_df):
        """Construye la estructura interna del chip."""
        return {
            "metadata": metadata_df.to_dict(orient="records"),
            "devices": devices_df.to_dict(orient="records"),
            "ports": ports_df.to_dict(orient="records")
        }
    
    def _build_measurement_plan(self, measurements_df):
        """Construye el plan de medida."""
        return measurements_df.to_dict(orient="records")
    
    def plot(self):
        """
        Muestra el contenido del chip.
        """
        if self.chip is None:
            print("No hay chip cargado.")
            return
        
        print("=" * 80)
        print("CHIP")
        print("=" * 80)
        pprint(self.chip)


# ======================================================
# FUNCIONES DE COMPATIBILIDAD (opcional)
# ======================================================

def load_chip(excel_file):
    """
    Función de compatibilidad con el código antiguo.
    """
    manager = ChipManager(excel_file)
    return manager.chip, manager.measurement_plan


def plot_chip(chip):
    """
    Función de compatibilidad con el código antiguo.
    """
    print("=" * 80)
    print("CHIP")
    print("=" * 80)
    pprint(chip)


# ======================================================
# EJEMPLO DE USO
# ======================================================

if __name__ == "__main__":
    # Usando la clase
    chip = ChipManager("chip_layout.xlsx")
    chip.plot()
    
    # También puedes cargar después de crear
    chip2 = ChipManager()
    chip2.load_chip("otro_chip.xlsx")
    chip2.plot()