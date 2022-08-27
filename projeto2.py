
class Professor():
    def __init__(self, id, habilitacoes, preferencias):
        self.id = id
        self.habilitacoes = int(habilitacoes)
        self.preferencias = preferencias
        self.contratado = 0
        self.contratante = ""
        self.rejeicoes = []
    
    def info(self):
        print("ID", self.id)
        print("Habilitacoes", self.habilitacoes)
        print("Preferencias", self.preferencias)
        print("Contratante", self.contratante)
        print("Rejeicoes", self.rejeicoes)

    

class Escola():
    def __init__(self, id, habilitacoes):
        self.id = id
        self.habilitacoes_pretendidas = [int(x) for x in habilitacoes]
        self.habilitacoes_obtidas = []
        self.vagas = len(habilitacoes)
        self.contratados = []

    def info(self):
        print("ID", self.id)
        print("Habilitacoes desejadas", self.habilitacoes_pretendidas)
        print("Contratados", self.contratados)
        print("Habilitacoes obtidas", self.habilitacoes_obtidas)


# lê dados do arquivo e guarda os professores e escolas em duas listas        
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


def melhor_escola_possivel(prof):
    for esc_id in prof.preferencias:
        if prof.habilitacoes >= min(escolas[esc_id].habilitacoes_pretendidas):
            return esc_id


def condition(professores):
    aplicantes = []
    for prof in professores.values():
        if prof.contratado == 0 and (prof.preferencias != []):
            aplicantes.append(prof.id)
    return aplicantes


def dispensa(idx, esc_id):
    prof_id = escolas[esc_id].contratados[idx]
    professores[prof_id].contratado = 0
    professores[prof_id].contratante = ""
    professores[prof_id].rejeicoes.append(esc_id)
    professores[prof_id].preferencias.remove(esc_id)

    escolas[esc_id].contratados.pop(idx)
    escolas[esc_id].habilitacoes_obtidas.pop(idx)

def restringir_preferencias():
    for prof_id in professores:
        to_remove = []
        for esc_id in professores[prof_id].preferencias:
            if professores[prof_id].habilitacoes < min(escolas[esc_id].habilitacoes_pretendidas):
                to_remove.append(esc_id)
        for x in to_remove:
            professores[prof_id].preferencias.remove(x)


def emparelhamentoEstavel():
    restringir_preferencias()
    disponiveis = condition(professores)
    while (disponiveis != []):
        prof_id = disponiveis[0]
        print("Antes")
        professores[prof_id].info()
        esc_id = melhor_escola_possivel(professores[prof_id])
        escolas[esc_id].info()
        escolas[esc_id].contratados.append(prof_id)
        escolas[esc_id].habilitacoes_obtidas.append(professores[prof_id].habilitacoes)

        professores[prof_id].contratado = 1
        professores[prof_id].contratante = esc_id

        if (len(escolas[esc_id].contratados) > escolas[esc_id].vagas):
            pior_aplicante_idx = escolas[esc_id].habilitacoes_obtidas.index(min(escolas[esc_id].habilitacoes_obtidas))
            dispensa(pior_aplicante_idx, esc_id)

        if (len(escolas[esc_id].contratados) == escolas[esc_id].vagas):
            hab = min(escolas[esc_id].habilitacoes_obtidas)
            for prof in professores.values():
                if (esc_id in prof.preferencias) and (prof.habilitacoes < hab):
                    prof.preferencias.remove(esc_id)

        print("Depois")
        professores[prof_id].info()
        escolas[esc_id].info()
        disponiveis = condition(professores)

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

