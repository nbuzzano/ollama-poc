import os
import csv as _csv


def local_file_search(query: str, base_dir: str = '.') -> str:
    q = (query or "").strip().lower()
    if not q:
        return "Consulta vacía. Escribe palabras claves para buscar en archivos .txt o .csv."

    max_results = 30
    matches = []

    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not (fname.lower().endswith('.txt') or fname.lower().endswith('.csv')):
                continue
            path = os.path.join(root, fname)
            try:
                if fname.lower().endswith('.txt'):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f):
                            if q in line.lower():
                                snippet = line.strip()
                                matches.append(f"{path} - L{i+1}: {snippet}")
                                if len(matches) >= max_results:
                                    break
                else:
                    with open(path, newline='', encoding='utf-8', errors='ignore') as f:
                        reader = _csv.reader(f)
                        for i, row in enumerate(reader):
                            rowtext = ' | '.join(row)
                            if q in rowtext.lower():
                                matches.append(f"{path} - R{i+1}: {rowtext}")
                                if len(matches) >= max_results:
                                    break
            except Exception:
                continue
        if len(matches) >= max_results:
            break

    if not matches:
        return f"No se encontraron coincidencias en archivos .txt/.csv bajo {base_dir}"

    return "\n".join(matches[:max_results])


if __name__ == '__main__':
    print('Buscando "agent" en el repo...')
    print(local_file_search('agent', base_dir='.'))
