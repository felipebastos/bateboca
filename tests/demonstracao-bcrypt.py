# Exemplo de hash:
# Versão: $2b$
# Custo: 12$
# Salt: zZlStYj5ZtBwbmhdL7lNTe
# Hash: tYL5b2CFHGDnhQvjukxcb1XIpKTpfVy

import timeit # usar para demonstrar quanto tempo leva para executar
import bcrypt # módulo já instalado

# A linha abaixo realiza apenas o hash de uma senha simples
# com o 'custo' de processamento na variável rodadas
# senha = bcrypt.hashpw(b'12345678', bcrypt.gensalt(rounds=rodadas))

# esta função recebe uma senha e as rodadas para o custo
def criptografe(senha, rodadas):
    senha = bcrypt.hashpw(senha, bcrypt.gensalt(rounds=rodadas))
    hashes.append(senha)

# esta função checa uma senha
def checando(senha_tentada, senha):
    bcrypt.checkpw(senha_tentada, senha)

senhas = [b'123456', b'12345678', b'1234567890', b'!@X#$*&()(-_!aH~']
hashes = []
for senha in senhas:
    print('Cronometrando para senha: {}'.format(senha))
    for x in range(4, 16):
        print('Com {} de custo'.format(x))
        print('Tempo: ', end='')
        print(timeit.timeit(lambda: criptografe(senha, x), number=5))

for senha in senhas:
    for senha_tentada in senhas:
        for senha in hashes:
            print('Cronometrando checagem para {} contra {}'.format(senha_tentada, senha))
            print(timeit.timeit(lambda: checando(senha_tentada, senha), number=5))
    
    
