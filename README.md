# PYOS Bootloader + JellyBean Kernel

A minimal Python-based bootloader and kernel simulation.

---

## Structure

- **bootloader.py** – Lists and boots `.pyboot` entries  
- **entries/** – Contains boot entries and kernels  
  - **main_entry.pyboot** – Defines OS name, version, and kernel path  
  - **Kernel/JellyBean/** – Simple kernel with a basic shell  

---

## How It Works

1. `bootloader.py` scans `entries/` for `.pyboot` files.  
2. You select an entry via a text UI (`py_cui`).  
3. It reads the kernel config (`config.pyos`) and runs its `main.py`.  
4. The JellyBean kernel provides a minimal shell (`help`, `cls`, `exit`).  

---

## Run

```bash
pip install py-cui termcolor
python bootloader.py

## Contact & Links

- [Portfolio](https://akshprooo.vercel.app)
- [GitHub](https://github.com/akshprooo)
- [Instagram](https://instagram.com/akshprooo.in)
- Discord: `@akshprooo`
- [Email](mailto:akshprooo@gmail.com)
