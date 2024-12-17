# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:07:58 2024

@author: Derson
"""

import os

def generate_tree(directory, prefix=""):
    dirNoListed = ['volumes','.git','.spyproject','.pytest_cache', 'development','__pycache__']
    entries = list(filter(lambda d : d not in dirNoListed
                          , os.listdir(directory)))
    entries.sort()  # Ordena para uma exibição consistente
    
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1
        
        connector = "└── " if is_last else "├── "
        
        print(f"{prefix}{connector}{entry}")
        
        if os.path.isdir(path):
            # Adiciona prefixo para subdiretórios
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(path, new_prefix)

# Executa o script no diretório atual ou substitua pelo caminho desejado
if __name__ == "__main__":
    #project_directory = "expense_cnt"  # Substitua pelo caminho do projeto
    project_directory = '.'
    print(f"{project_directory}/")
    generate_tree(project_directory)
