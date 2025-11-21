import re
import pandas as pd

input_file = "output/unmapped_roles.txt"
output_file = "dictionary/mapped_roles_full.csv"

# Load the file
with open(input_file, 'r') as f:
    lines = f.readlines()

data = []
for line in lines:
    # Extract count and role using regex
    match = re.search(r'^\s*(\d+)x\s+(.*)$', line)
    if match:
        data.append({'role': match.group(2).strip(), 'count': int(match.group(1))})

df = pd.DataFrame(data)

def normalize_role(role_str):
    r = role_str.lower().strip()
    r_clean = r.replace('-', '').replace(' ', '')
    
    # 1. Specific Co-Roles
    if any(x in r for x in ['co-tutor', 'cotutor', 'cotutore']): return 'co-tutor'
    if any(x in r for x in ['co-supervisor', 'cosupervisor', 'correlatore', 'correlatrice']): return 'co-supervisor'
    if any(x in r for x in ['co-advisor', 'coadvisor']): return 'co-advisor'
    if any(x in r for x in ['co-director', 'codirector']): return 'co-director'
    if any(x in r for x in ['co-examiner', 'controrelatore']): return 'co-examiner'
    
    # 2. Main Roles
    if 'coordinator' in r_clean or 'coordinat' in r_clean or 'coord.' in r: return 'coordinator'
    
    if 'tutor' in r or 'tutore' in r or 'tutrice' in r:
        if any(x in r for x in ['estern', 'external', 'foreign']): return 'external tutor'
        if any(x in r for x in ['aziendal', 'company', 'industri']): return 'company tutor'
        return 'tutor'
        
    if 'supervis' in r or 'relator' in r or 'guida' in r:
        if any(x in r for x in ['estern', 'external']): return 'external supervisor'
        if 'intern' in r: return 'internal supervisor'
        return 'supervisor'
        
    if any(x in r for x in ['direct', 'direttor', 'head', 'responsabile', 'chair', 'dos']):
        if any(x in r for x in ['ricerca', 'research']): return 'research director'
        return 'program director'
        
    if 'presiden' in r: return 'president'
    if any(x in r for x in ['candidat', 'author', 'autore']): return 'candidate'
    if any(x in r for x in ['dottorand', 'student', 'alliev', 'phd']): return 'phd student'
    if any(x in r for x in ['referee', 'review', 'revisore', 'rapporteur', 'opponent', 'reader']): 
        if any(x in r for x in ['estern', 'external']): return 'external referee'
        return 'referee'
    if any(x in r for x in ['member', 'membro', 'componente', 'commissari', 'committee', 'jury']): return 'committee member'
    if any(x in r for x in ['docent', 'prof', 'faculty']): return 'professor'
    if any(x in r for x in ['advisor', 'adviser', 'consiglier']): return 'advisor'
    
    # 3. Metadata & Other
    if any(x in r for x in ['sede', 'consorz', 'universit', 'dipartimento', 'department', 'school', 'scuola']): return 'institution'
    if 'tesi' in r or 'thesis' in r: return 'thesis info'

    return 'other'

df['normalized_role'] = df['role'].apply(normalize_role)
df[['role', 'normalized_role']].to_csv(output_file, index=False)
print("Mapping complete.")