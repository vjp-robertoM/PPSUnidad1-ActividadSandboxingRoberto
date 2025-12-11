# Prueba de aplicaciones en un entorno de ejecución controlado (Sandboxing)

En este apartado se describe cómo se creó un **entorno de ejecución aislado** para probar la aplicación `lavadero.py` utilizando **Firejail** y su interfaz gráfica **Firetools**. El objetivo es ejecutar la aplicación de manera segura, sin comprometer el sistema operativo principal, y documentar el proceso.

---

## 1. Preparación del entorno sandbox

Para garantizar la seguridad y el aislamiento del sistema, se siguieron los siguientes pasos:

### 1.1 Instalación de Firejail y Firetools

1. Actualizar los repositorios del sistema:

```bash
sudo apt update
sudo apt install firejail -y
sudo apt install firetools -y
```


2. Crear un entorno virtual de Python

```bash
python3 -m venv .venv       # Crear entorno virtual
source .venv/bin/activate   # Activar entorno virtual
which python                # Comprobar que apunta al Python del entorno
python --version            # Ver versión de Python
```
3. Ejecutar pruebas unitarias en sandbox

```bash
PYTHONPATH=src firejail --private=.venv python3 -m unittest tests/test_lavadero_custom.py -v
```
Esto asegura que tanto la ejecución como las pruebas se hacen en un entorno controlado.
