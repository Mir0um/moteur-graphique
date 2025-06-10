# Contributor Guidelines

Please follow these conventions when working with this repository:

- **Style**: Adhere to [PEP 8](https://peps.python.org/pep-0008/) coding style.
- **Compilation check**: Before committing, run:
  ```bash
  python -m py_compile main.py moteur_graphique.py lib_math.py keyboard_library.py
  ```
  Ensure there are no compilation errors.
- **Models**: `.obj` files for 3D models are stored in the `object/` directory.
- **Running**: Start the engine with:
  ```bash
  python main.py
  ```
