import os
from datetime import datetime, timedelta
import random
import re
from colorama import Fore, Back, Style
from tui import Oblivion_UI
import threading
import sys
import typer 
from rich.console import Console
from rich.panel import Panel
app = typer.Typer()
console = Console()

CHAR_LIMIT = 256
MIN_LIMIT = 10
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
@app.command("init")
def initialize_vault():
    base = get_base_path()
    folder_name = "oblivion"
    file_name = "oblivion.md"
    vault_dir = os.path.join(base, folder_name)
    full_path = os.path.join(vault_dir,file_name)

    os.makedirs(vault_dir, exist_ok=True)

    if not os.path.exists(full_path):
        with open(full_path, 'w') as f:
            f.write("# Oblivion - The LAW of Thought \n\n")
    return full_path
@app.command("add")
def creat_atom(content: str):
    signal = content
    if len(signal) > CHAR_LIMIT:
        print("To many characters, destill your thoughts")
        return f"To many characters, destill your thoughts"
    if len(signal) < MIN_LIMIT: 
        print(f"Enter the minimum of 10" )
        return f"Enter the minimum of 10" 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(signal) == 0:
        return "Enter an Atom"
    db_path = initialize_vault()
    try: 
        with open(db_path, 'a', encoding="utf-8") as f:
            entry = f"{timestamp} | {signal} \n"
            f.write(entry)
        console.print(Panel(f"[bold cyan]Atom secure[/][italic]. ({len(signal)} chars)[/]"))
        return {"timestamp": timestamp,"Content": signal,}
    except Exception as e:
        print(f"Critical Failure: {e}")
     
@app.command("whisper")
def whisper():
        """
        Retrieves a single random thought from the void.
        Time Complexity: O(n)
        """

        db_path = initialize_vault()
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                atoms = [line.strip() for line in f.readlines() if "|" in line and line.split("|")[1].strip()]
            if not atoms:
                print("The Keep is silent (File is empty).")
                return 
                
            selection = random.choice(atoms).strip()
            print("\n" + ("-" * 40))
            console.print(Panel(f"[bold red]{selection}[/]",title="whisper"))
            print(("-" * 40) + "\n")
            return selection
        except Exception as e:
            print(f"Critical Failure: {e}")
            return None
@app.command("query")
def query(query: str):
    """
    Docstring for search_atoms
    
    :param query_terms: Scans the vault for lines containing ALL query terms (order agnostic).
    """
    if hasattr(query, 'query'):
        query_terms = query
    elif isinstance(query, str):
        query_terms = query.split()
    else: 
        query_terms = query
    terms = "^" + "".join([f"(?=.*{re.escape(term)})" for term in query_terms])
    db_path = initialize_vault()
    found_count = 0 
    results = []
    with open(db_path, "r", encoding="utf-8") as f:
        for line in f:
            if re.search(terms, line, re.IGNORECASE):
                print(line.strip())
                results.append(line.strip())
                found_count += 1

    if not results:
        return "No atoms found in the void"
    return "\n".join(results)
@app.command("count")
def atom_count():
    db_path = initialize_vault()
    count = 0
    with open(db_path, 'r', encoding="utf-8") as f: 
        for line in f:
            count += 1
    print(f"Atoms:{count}")
@app.command("decay")
def atom_decay():
    '''
       This caluclates the rate of decay. 30 days will get a light red, more a black.  
    '''
    formating_string = "%Y-%m-%d"
    current = datetime.now()
    thirty_days_ago = current - timedelta(days=30)
    more_days_ago = current - timedelta(days=90)
    db_path = initialize_vault()
    with open(db_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            time = word.split()
            
            
            if not word:
                continue
            file_datatime = datetime.strptime(time[0], formating_string)
            if file_datatime > thirty_days_ago:

                print(Fore.RED + word)
            if file_datatime > more_days_ago:
                print(Style.DIM + word + Fore.BLACK)


@app.command("Obi")
def oblivion_tui():
    app = Oblivion_UI()
    app.run()

        
def detect(args):
    db_path = initialize_vault()
    with open(db_path, 'r', encoding='utf-8') as f:
        for line in f: 
            if line[1]  == "":
                line.strip()
