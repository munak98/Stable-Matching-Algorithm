
class Professor():
    def __init__(self, id, habilitacoes, preferencias):
        self.id = id
        self.habilitacoes = int(habilitacoes)
        self.preferencias = preferencias
        self.contratado = 0
        self.contratante = ""
        self.rejeicoes = []
    
class Escola():
    def __init__(self, id, habilitacoes):
        self.id = id
        self.habilitacoes_pretendidas = [int(x) for x in habilitacoes]
        self.habilitacoes_obtidas = []
        self.contratados = []
        self.candidatos_possiveis = []


# lê dados do arquivo e guarda os professores e escolas em dois dicionarios        
with open("projetoTAG.txt", "r") as file:
    professores = {}
    escolas = {}
    for line in file:
        if not line.startswith("("):
            continue
        line = line.replace(" ", "").replace("\n", "").replace("(", "").replace(")", "").replace(":", ",")
        line = line.split(",")
        if line[0].startswith("P"):
            professores[line[0]] = Professor(line[0], line[1], line[2:])
        if line[0].startswith("E"):
            escolas[line[0]] = Escola(line[0], line[1:])

def desempregados_com_opcao(professores):
    aplicantes = []
    for prof in professores.values():
        if prof.contratado == 0 and (len(prof.preferencias) != len(prof.rejeicoes)):
            aplicantes.append(prof.id)
    return aplicantes

def contrata(esc_id, prof_id):
    escolas[esc_id].contratados.append(prof_id)
    escolas[esc_id].habilitacoes_obtidas.append(professores[prof_id].habilitacoes)

    professores[prof_id].contratado = 1
    professores[prof_id].contratante = esc_id

def dispensa(esc_id, idx):
    prof_id = escolas[esc_id].contratados[idx]
    professores[prof_id].contratado = 0
    professores[prof_id].contratante = ""
    professores[prof_id].rejeicoes.append(esc_id)

    escolas[esc_id].contratados.pop(idx)
    escolas[esc_id].habilitacoes_obtidas.pop(idx)
    escolas[esc_id].candidatos_possiveis.remove(prof_id)

def melhor_escola_possivel(prof_id):
    for esc_id in professores[prof_id].preferencias:
        if prof_id in escolas[esc_id].candidatos_possiveis:
            return esc_id
    return -1

def emparelhamentoEstavel():
    for prof_id in professores:
        for esc_id in professores[prof_id].preferencias:
            if professores[prof_id].habilitacoes >= min(escolas[esc_id].habilitacoes_pretendidas):
                escolas[esc_id].candidatos_possiveis.append(prof_id)
            else:
                professores[prof_id].rejeicoes.append(esc_id)

    disponiveis = desempregados_com_opcao(professores)

    while (disponiveis != []):
        prof_id = disponiveis[0]
        esc_id = melhor_escola_possivel(prof_id)

        print(vars(professores[prof_id]))
        print(vars(escolas[esc_id]))
        
        contrata(esc_id, prof_id)

        n_contratados = len(escolas[esc_id].contratados)
        vagas = len(escolas[esc_id].habilitacoes_pretendidas)

        if (n_contratados > vagas):
            pior_idx = escolas[esc_id].habilitacoes_obtidas.index(min(escolas[esc_id].habilitacoes_obtidas))
            dispensa(esc_id, pior_idx)

        if (n_contratados == vagas):
            min_hab = min(escolas[esc_id].habilitacoes_obtidas)
            for candidato in escolas[esc_id].candidatos_possiveis:
                if professores[candidato].habilitacoes < min_hab:
                    escolas[esc_id].candidatos_possiveis.remove(candidato)
                    professores[candidato].rejeicoes.append(esc_id)


        disponiveis = desempregados_com_opcao(professores)

def teste():
    for esc in escolas.values():
        assert len(esc.contratados) <= esc.vagas
        assert len(esc.contratados) >= 1

def print_emparelhamento():
    count = 0
    for prof in professores.values():
        if prof.contratante != "":
            count += 1
        print(f"{prof.id}: {prof.contratante}")
    print("Tamanho do emparelhamento: ", count)

def print_emparelhamento2():
    for esc in escolas.values():
        print(esc.id, esc.contratados)

emparelhamentoEstavel()
print_emparelhamento2()
print_emparelhamento()

