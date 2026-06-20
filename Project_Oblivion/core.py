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
def create_atoms(content:str):
    signal = content
    if len(signal) > CHAR_LIMIT:
        return f"To many characters, destill your thoughts"
    if len(signal) < MIN_LIMIT:
        return f"Enter the minimum of 10" 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db_path = initialize_vault()
    try: 
        with open(db_path, 'a', encoding="utf-8") as f:
            entry = f"{timestamp} | {signal} \n"
            f.write(entry)
        return {"timestamp": timestamp,"Content": signal,}
    except Exception as e:
        print(f"Critical Failure: {e}")


@app.command("add")
def create_atom(content: str = typer.Argument(None)):
    if content is None or len(content.strip()) == 0:
        content = typer.prompt("Enter content here")
    signal = content
    if len(signal) > CHAR_LIMIT:
        console.print("[bold cyan]To many characters, destill your thoughts[/]")
        return f"To many characters, destill your thoughts"
    if len(signal) < MIN_LIMIT: 
        console.print(f"[bold red]Enter the minimum of 10[/]" )
        return f"Enter the minimum of 10" 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    atom = create_atoms(signal)
    console.print(f"[bold cyan]{atom}")
     
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
def query(query_input: str) -> list[str]:
    """
    Docstring for search_atoms
    
    :param query_terms: Scans the vault for lines containing ALL query terms (order agnostic).
    """
    if hasattr(query, 'query'):
        query_terms = query_input
    elif isinstance(query, str):
        query_terms = query_input.split()
    else: 
        query_terms = query_input
    terms = "^" + "".join([f"(?=.*{re.escape(term)})" for term in query_terms])
    db_path = initialize_vault()
    found_count = 0 
    results = []
    with open(db_path, "r", encoding="utf-8") as f:
        for line in f:
            if re.search(terms, line, re.IGNORECASE):
                results.append(line.strip())
                

    return results
@app.command("querys")
def query_command(query_str: str = typer.Argument(None), interactive: bool = True):
    """
    Docstring for search_atoms
    
    :param query_terms: Scans the vault for lines containing ALL query terms (order agnostic).
    """
    if query_str is None or len(query_str.strip()) == 0 and interactive == True:
        query_str = typer.prompt("Enter query here")
    if not query_str or len(query_str.strip()) == 0:
        console.print("[bold red] No query terms procided. [/]")
        raise typer.Exit()
    results = query(query_str)

    if not results:
        console.print("[bold yellow] No atoms found in the void[/]")
        return
    for line in results: 
        console.print(Panel(f"[bold cyan][italic. {line}[/]]", title="Query"))
        

@app.command("count")
def atom_count():
    db_path = initialize_vault()
    count = 0
    with open(db_path, 'r', encoding="utf-8") as f: 
        for line in f:
            count += 1
    console.print(f"[bold cyan]Atoms:{count}[/]")
def get_decayed_atoms() -> list[tuple[str, str]]:
    formating_string = "%Y-%m-%d"
    current = datetime.now()
    thirty_days_ago = current - timedelta(days=30)
    more_days_ago = current - timedelta(days=90)

    db_path = initialize_vault()
    results = []
    with open(db_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            # 1. Skip comments or empty structural lines safely
            if not stripped_line or stripped_line.startswith("#") or " | " not in stripped_line:
                continue
                
            # 2. Safely unpack by our explicit delimiter
            timestamp_part, content = stripped_line.split(" | ", 1)
            
            # Extract just the 'YYYY-MM-DD' sub-component
            date_str = timestamp_part.split()[0] 
            
            try:
                file_datetime = datetime.strptime(date_str, formating_string)
            except ValueError:
                continue # Skip corrupted or malformed date inputs
                
            # 3. Use an inverted chronological if/elif chain
            if file_datetime < more_days_ago:
                results.append(("DEAD", stripped_line))
            elif file_datetime < thirty_days_ago:
                results.append(("DECAYING", stripped_line))
                
    return results

@app.command("decay")
def atom_decay():
    '''
       This caluclates the rate of decay. 30 days will get a light red, more a black.  
    '''
    dead = get_decayed_atoms()
    console.print(Panel(f"[bold red]{dead}[/]", title="Decay Atoms"))


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
