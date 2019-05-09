#coding: utf-8

import random
import wx

class meuFrame(wx.Frame):
    valoresVencedores = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    ultimaJogada = None

    nivelDificuldade = 1

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        sizerPrincipal = wx.BoxSizer(wx.VERTICAL)

        self.nomeUsuario = wx.GetTextFromUser("Insira o nome do jogador:", "", default_value="Jogador 1")
        while not self.nomeUsuario:
            self.nomeUsuario = wx.GetTextFromUser("Insira o nome do jogador:", "", default_value="Jogador 1")

        textoBemVindo = wx.StaticText(self, label="Seja bem Vindo, "+self.nomeUsuario+"!")
        sizerPrincipal.Add(textoBemVindo)

        self.dicionarioVez = {
            "X": wx.Bitmap("x.png", wx.BITMAP_TYPE_PNG),
            "O": wx.Bitmap("o.png", wx.BITMAP_TYPE_PNG),
            "BLANK": wx.Bitmap('blank.png', wx.BITMAP_TYPE_PNG)
        }
        
        self.vezDe = "X"

        _00 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _01 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _02 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        
        _10 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _11 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _12 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        
        _20 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _21 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)
        _22 = wx.BitmapButton(self, size=(32,32), style=wx.BU_NOTEXT)

        self.botoes = [
            [_00, _01, _02],
            [_10, _11, _12],
            [_20, _21, _22]
        ]
        
        self.posicoesDisponiveis = []

        for linha in self.botoes:
            sizerLinha = wx.BoxSizer(wx.HORIZONTAL)
            for botao in linha:
                botao.SetLabelText('')
                botao.SetBitmap(self.dicionarioVez['BLANK'])
                self.posicoesDisponiveis.append(botao)
                botao.Bind(wx.EVT_BUTTON, self.marcar_jogada_do_usuario)
                sizerLinha.Add(botao, 1, wx.CENTER | wx.EXPAND)

            sizerPrincipal.Add(sizerLinha, 1, wx.CENTER | wx.EXPAND)

        nivelDeDificuldade = wx.Choice(self, choices=['Fácil', 'Médio', 'Difícil'])
        nivelDeDificuldade.SetSelection(1)
        
        botaoResetarJogo = wx.Button(self, label="Resetar")
        # BINDS
        nivelDeDificuldade.Bind(wx.EVT_CHOICE, self.mudar_dificuldade)
        botaoResetarJogo.Bind(wx.EVT_BUTTON, self.resetar_jogo)
        # BINDS

        sizerConfiguracoes = wx.BoxSizer(wx.HORIZONTAL)

        sizerConfiguracoes.Add(nivelDeDificuldade, 0, wx.CENTER | wx.EXPAND)
        sizerConfiguracoes.Add(botaoResetarJogo,   0, wx.CENTER | wx.EXPAND)

        sizerPrincipal.Add(sizerConfiguracoes, 0, wx.CENTER)

        self.SetSizer(sizerPrincipal)
        self.SetAutoLayout(1)
        sizerPrincipal.Fit(self)
        self.Show()

    def mudar_dificuldade(self, event):
        self.nivelDificuldade = event.GetInt()

    def verificar_vitoria(self):
        for possibilidade in self.valoresVencedores:
            posicao1 = possibilidade[0] 
            posicao2 = possibilidade[1]
            posicao3 = possibilidade[2]
            
            valorBotaoUm   = self.botoes[posicao1[0]][posicao1[1]].GetLabelText()
            valorBotaoDois = self.botoes[posicao2[0]][posicao2[1]].GetLabelText()
            valorBotaoTres = self.botoes[posicao3[0]][posicao3[1]].GetLabelText()

            if valorBotaoUm == valorBotaoDois == valorBotaoTres != '':
                return 1

        if len(self.posicoesDisponiveis) == 0:
            return 2

        return -1

    def resetar_jogo(self, event=None):
        self.posicoesDisponiveis = []
        
        for linha in self.botoes:
            for botao in linha:
                self.posicoesDisponiveis.append(botao)
                botao.SetLabelText('')
                botao.SetBitmap(self.dicionarioVez['BLANK'])
                botao.Enable()

        self.marcar_jogada_do_pc()

    def obter_melhor_jogada_facil(self):
        return random.choice(self.posicoesDisponiveis)

    def analisar_possibilidades(self):
        vezDe = 'X' if self.vezDe == 'O' else 'O'
        self.posicoesMaisPossiveis = {
            'ataque': {
                1: [],
                2: []
            },
            'defesa': {
                1: [],
                2: []
            },
            'neutros': {
                0: []
            }
        }

        for possibilidade in self.valoresVencedores:
            posicao1 = possibilidade[0] 
            posicao2 = possibilidade[1]
            posicao3 = possibilidade[2]
            
            valorBotaoUm   = self.botoes[posicao1[0]][posicao1[1]].GetLabelText()
            valorBotaoDois = self.botoes[posicao2[0]][posicao2[1]].GetLabelText()
            valorBotaoTres = self.botoes[posicao3[0]][posicao3[1]].GetLabelText()

            posicoes = [posicao1, posicao2, posicao3]
            valoresDosBotoes = [valorBotaoUm, valorBotaoDois, valorBotaoTres]
            valoresX = valoresDosBotoes.count("X")
            valoresO = valoresDosBotoes.count("O")

            if valoresX + valoresO == 3:
                continue
            elif valoresX == valoresO:
                possibilidade = 0
                posicao       = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                self.posicoesMaisPossiveis['neutros'][possibilidade].append(posicao)
            
            elif valoresX == 2:
                possibilidade = 2
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'X':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            elif valoresX == 1:
                possibilidade = 1
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'X':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)

            elif valoresO == 2:
                possibilidade = 2
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'O':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            elif valoresO == 1:
                possibilidade = 1
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'O':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            
            else:
                print("OPPAA!! NÃO PREVI ISSO!!!")

    def obter_melhor_jogada_medio(self, defesaOuAtaque=-1):
        wx.BeginBusyCursor()

        self.analisar_possibilidades()
        
        try:
            print(self.posicoesMaisPossiveis)
            if defesaOuAtaque == -1:
                numeroDefesas = len(self.posicoesMaisPossiveis['defesa'][1]) + len(self.posicoesMaisPossiveis['defesa'][2])
                numeroAtaques = len(self.posicoesMaisPossiveis['ataque'][1]) + len(self.posicoesMaisPossiveis['ataque'][2])
                
                if numeroDefesas > 0 and numeroAtaques > 0:
                    defesaOuAtaque = random.choice(['defesa', 'ataque'])
                
                elif numeroAtaques > 0:
                    defesaOuAtaque = 'ataque'
                
                elif numeroDefesas > 0:
                    defesaOuAtaque = 'defesa'
                
                else:
                    defesaOuAtaque = 'neutros'

            if 0 not in self.posicoesMaisPossiveis[defesaOuAtaque]:
                if len(self.posicoesMaisPossiveis[defesaOuAtaque][2]) > 0:
                    melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][2])
                elif len(self.posicoesMaisPossiveis[defesaOuAtaque][1]) > 0:
                    melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][1])
                else:
                    wx.EndBusyCursor()
                    return False
            else:
                melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][0])
            
            botao = self.botoes[melhorPosicao[0]][melhorPosicao[1]]
        except IndexError: # posicoesMaisPossiveis está vazia
            botao = False
        wx.EndBusyCursor()
        return botao

    def obter_melhor_jogada_dificil(self, defesaOuAtaque=-1):
        wx.BeginBusyCursor()

        self.analisar_possibilidades()

        vezDe = 'X' if self.vezDe == 'O' else 'O'
        self.posicoesMaisPossiveis = {
            'ataque': {
                1: [],
                2: []
            },
            'defesa': {
                1: [],
                2: []
            },
            'neutros': {
                0: []
            }
        }

        for possibilidade in self.valoresVencedores:
            posicao1 = possibilidade[0] 
            posicao2 = possibilidade[1]
            posicao3 = possibilidade[2]
            
            valorBotaoUm   = self.botoes[posicao1[0]][posicao1[1]].GetLabelText()
            valorBotaoDois = self.botoes[posicao2[0]][posicao2[1]].GetLabelText()
            valorBotaoTres = self.botoes[posicao3[0]][posicao3[1]].GetLabelText()

            posicoes = [posicao1, posicao2, posicao3]
            valoresDosBotoes = [valorBotaoUm, valorBotaoDois, valorBotaoTres]
            valoresX = valoresDosBotoes.count("X")
            valoresO = valoresDosBotoes.count("O")

            if valoresX + valoresO == 3:
                continue
            elif valoresX == valoresO:
                possibilidade = 0
                posicao       = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                self.posicoesMaisPossiveis['neutros'][possibilidade].append(posicao)
            
            elif valoresX == 2:
                possibilidade = 2
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'X':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            elif valoresX == 1:
                possibilidade = 1
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'X':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)

            elif valoresO == 2:
                possibilidade = 2
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'O':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            elif valoresO == 1:
                possibilidade = 1
                posicao = [posicao for posicao in posicoes if self.botoes[posicao[0]][posicao[1]].GetLabelText() == ''][0]
                
                if vezDe is 'O':
                    self.posicoesMaisPossiveis['ataque'][possibilidade].append( posicao )
                else:
                    self.posicoesMaisPossiveis['defesa'][possibilidade].append(posicao)
            
            else:
                print("OPPAA!! NÃO PREVI ISSO!!!")
        
        try:
            print(self.posicoesMaisPossiveis)
            if defesaOuAtaque == -1:
                numeroDefesas = len(self.posicoesMaisPossiveis['defesa'][1]) + len(self.posicoesMaisPossiveis['defesa'][2])
                numeroAtaques = len(self.posicoesMaisPossiveis['ataque'][1]) + len(self.posicoesMaisPossiveis['ataque'][2])
                
                if numeroDefesas > 0 and numeroAtaques > 0:
                    maioresValores = {b: (len(self.posicoesMaisPossiveis[b][1]), len(self.posicoesMaisPossiveis[b][2]))
                                     for b in self.posicoesMaisPossiveis if b != 'neutros'}
                    maiorValoresPossibilidade1 = sorted(maioresValores, key=lambda x: maioresValores[x][0])[-1]
                    maiorValoresPossibilidade2 = sorted(maioresValores, key=lambda x: maioresValores[x][1])[-1]
                    
                    print(maioresValores)
                    if maioresValores[maiorValoresPossibilidade2][1] > 0:
                        defesaOuAtaque = maiorValoresPossibilidade2
                    else:
                        defesaOuAtaque = maiorValoresPossibilidade1
                    
                    #defesaOuAtaque = random.choice(['defesa', 'ataque'])
                
                elif numeroAtaques > 0:
                    defesaOuAtaque = 'ataque'
                
                elif numeroDefesas > 0:
                    defesaOuAtaque = 'defesa'
                
                else:
                    defesaOuAtaque = 'neutros'

            if 0 not in self.posicoesMaisPossiveis[defesaOuAtaque]:
                if len(self.posicoesMaisPossiveis[defesaOuAtaque][2]) > 0:
                    melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][2])
                elif len(self.posicoesMaisPossiveis[defesaOuAtaque][1]) > 0:
                    melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][1])
                else:
                    wx.EndBusyCursor()
                    return False
            else:
                melhorPosicao = random.choice(self.posicoesMaisPossiveis[defesaOuAtaque][0])
            
            botao = self.botoes[melhorPosicao[0]][melhorPosicao[1]]
        except IndexError: # posicoesMaisPossiveis está vazia
            botao = False
        wx.EndBusyCursor()
        return botao

    def marcar_jogada_do_pc(self):
        if self.nivelDificuldade == 0:
            botao = self.obter_melhor_jogada_facil()
        elif self.nivelDificuldade == 1:
            botao = self.obter_melhor_jogada_medio()
            botao = botao if botao else random.choice(self.posicoesDisponiveis)
        elif self.nivelDificuldade == 2:
            botao = self.obter_melhor_jogada_dificil()
            botao = botao if botao else random.choice(self.posicoesDisponiveis)
        
        self.marcar_jogada(botao, 1)

    def marcar_jogada_do_usuario(self, event):
        botaoClicado = event.GetEventObject()
        
        if botaoClicado in self.posicoesDisponiveis:
            self.marcar_jogada(botaoClicado, self.nomeUsuario)
        else:
            event.Skip()
            return

    def terminar_jogo(self, jogador):
        for linha in self.botoes:
            for botao in linha:
                botao.Disable()

        if isinstance(jogador, str):
            mensagem = "Parabéns, você ganhou o jogo!"
        else:
            if jogador == 1:
                mensagem = "Que pena, " + self.nomeUsuario + " você se lascou!"
            else:
                mensagem = "Deu velha!"
        
        wx.MessageDialog(self, mensagem, "Notícia quentinha", wx.ICON_INFORMATION).ShowModal()

    def marcar_jogada(self, botao, jogador):
        botao.SetLabelText(self.vezDe)
        botao.SetBitmap(self.dicionarioVez[self.vezDe])
        
        if self.vezDe == 'X':
            self.vezDe = 'O'
        else:
            self.vezDe = 'X'

        self.posicoesDisponiveis.remove(botao)

        aJogadaEhGanhadora = self.verificar_vitoria()
        if aJogadaEhGanhadora == -1 and jogador != 1:
            self.marcar_jogada_do_pc()

        if aJogadaEhGanhadora == 1:
            self.terminar_jogo(jogador)
        elif aJogadaEhGanhadora == 2:# velha
            self.terminar_jogo(2)

def main():
    app = wx.App()
    janela = meuFrame(None, title="Jogo de velha")
    app.MainLoop()

if __name__ == '__main__':
    main()
