import pandas as pd


def get_selected_molecules():
    """
    Returns list of molecules from CSV
    """
    # Read the list of molecules
    molecules = pd.read_excel("data/gain-synonyms-list.xlsx")
    molecules_list = list(molecules['Gain'].str.lower())
    # selected_molecules = [m.split(" ")[-1] for m in molecules_list[0:7000] if (("+" not in m) and 

    selected_molecules = [m.split(" ")[-1] for m in molecules_list[0:7000] if (("+" not in m) and 
                        (m.endswith("olol") or 
                        m.endswith('cillin') or 
                        m.endswith('sartan') or 
                        m.endswith('mycin') or 
                        m.endswith('vir') or 
                        m.endswith('parin') or
                        m.endswith('mab') or 
                        m.endswith('lamide') or
                        m.endswith('caine') or
                        m.endswith('bital') or
                        m.endswith('afil') or
                        m.endswith('asone') or
                        m.endswith('profen') or 
                        m.endswith('statin') or
                        m.endswith('tinib')))]
    
    return selected_molecules