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

    pontuacaoUsuario = 0
    pontuacaoPC      = 0

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx.Colour(255,255,255))

        sizerPrincipal = wx.BoxSizer(wx.VERTICAL)

        self.nomeUsuario = wx.GetTextFromUser("Insira o nome do jogador:", "", default_value="Jogador 1")
        while not self.nomeUsuario:
            self.nomeUsuario = wx.GetTextFromUser("Insira o nome do jogador:", "", default_value="Jogador 1")

        self.textoBemVindo = wx.Button(self, style=wx.BORDER_NONE | wx.BU_EXACTFIT, size=(-1, 45))#label="Seja bem Vindo, "+self.nomeUsuario+"!")
        self.corPadraoDeBotao = wx.Colour(255, 255, 255)
        self.textoBemVindo.SetBackgroundColour(wx.Colour(255,255,255))
        textoMarkup = ''
        textoMarkup = ("<span foreground='black'>Seja bem-vindo,</span> <b>{nome}</b>!\n"
                       "Placar atual é: {nome}={pontuacaoUsuario} x PC={pontuacaoPC}").format(
            nome=self.nomeUsuario,
            pontuacaoUsuario=self.pontuacaoUsuario,
            pontuacaoPC=self.pontuacaoPC)
        self.textoBemVindo.SetLabelMarkup(textoMarkup)
        self.textoBemVindo.Disable()
        sizerPrincipal.Add(self.textoBemVindo, 0, wx.CENTER | wx.EXPAND | wx.ALL ^ wx.BOTTOM, 6)

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
                botao.SetBackgroundColour(wx.Colour(255, 255, 255))
                botao.SetBitmap(self.dicionarioVez['BLANK'])
                botao.SetWindowStyle(wx.BU_NOTEXT | wx.BORDER_NONE)
                botao.SetCursor(wx.Cursor(wx.CURSOR_HAND))

                self.posicoesDisponiveis.append(botao)
                botao.Bind(wx.EVT_BUTTON, self.marcar_jogada_do_usuario)
                botao.Bind(wx.EVT_ENTER_WINDOW, self.mudar_cor_botao)
                botao.Bind(wx.EVT_LEAVE_WINDOW, self.mudar_cor_botao)
                sizerLinha.Add(botao, 1, wx.CENTER | wx.EXPAND)
                if botao != linha[-1]:
                    sizerLinha.Add(wx.StaticLine(self, size=(1, 95), style=wx.LI_VERTICAL), 0, wx.CENTER | wx.LEFT, 5)

            sizerPrincipal.Add(sizerLinha, 1, wx.CENTER | wx.EXPAND | wx.ALL ^ wx.BOTTOM, 5)
            if linha != self.botoes[-1]:
                sizerPrincipal.Add(wx.StaticLine(self, size=(430, 1)), 0, wx.CENTER | wx.TOP, 5)

        textoNivelDeDificuldade = wx.StaticText(self, label="Nível de dificuldade:")
        nivelDeDificuldade = wx.Choice(self, choices=['Fácil', 'Médio', 'Difícil'])
        nivelDeDificuldade.SetSelection(1)
        
        botaoResetarJogo = wx.Button(self, label="Resetar")
        # BINDS
        nivelDeDificuldade.Bind(wx.EVT_CHOICE, self.mudar_dificuldade)
        botaoResetarJogo.Bind(wx.EVT_BUTTON, self.resetar_jogo)
        # BINDS

        sizerConfiguracoes = wx.BoxSizer(wx.HORIZONTAL)

        sizerConfiguracoes.Add(textoNivelDeDificuldade, 0, wx.CENTER | wx.RIGHT, 6)
        sizerConfiguracoes.Add(nivelDeDificuldade, 0, wx.CENTER | wx.RIGHT | wx.EXPAND, 6)
        sizerConfiguracoes.Add(botaoResetarJogo,   0, wx.CENTER | wx.EXPAND)

        sizerPrincipal.Add(sizerConfiguracoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizerPrincipal)
        self.SetAutoLayout(1)
        self.Center()
        # sizerPrincipal.Fit(self)
        self.Show()

    def mudar_cor_botao(self, evento):
        botao = evento.GetEventObject()
        if botao.GetBackgroundColour() != wx.Colour(0, 255, 0):
            if evento.Entering():
                botao.SetBackgroundColour(wx.Colour(*(243,)*3))
            elif evento.Leaving():
                botao.SetBackgroundColour(self.corPadraoDeBotao)

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
                for posicao in [posicao1, posicao2, posicao3]:
                    self.botoes[posicao[0]][posicao[1]].SetBackgroundColour(wx.Colour(0, 255, 0))
                return 1

        if len(self.posicoesDisponiveis) == 0:
            return 2

        return -1

    def resetar_jogo(self, event=None):
        if self.vezDe == 'X':
            self.vezDe = 'O'
        else:
            self.vezDe = 'X'
        
        self.posicoesDisponiveis = []
        
        for linha in self.botoes:
            for botao in linha:
                self.posicoesDisponiveis.append(botao)
                botao.SetLabelText('')
                botao.SetBackgroundColour(self.corPadraoDeBotao)
                botao.SetBitmap(self.dicionarioVez['BLANK'])
                botao.Enable()

        if self.vezDe is 'X':
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
        
        try:
            if defesaOuAtaque == -1:
                numeroDefesas = len(self.posicoesMaisPossiveis['defesa'][1]) + len(self.posicoesMaisPossiveis['defesa'][2])
                numeroAtaques = len(self.posicoesMaisPossiveis['ataque'][1]) + len(self.posicoesMaisPossiveis['ataque'][2])
                
                if numeroDefesas > 0 and numeroAtaques > 0:
                    maioresValores = {b: (len(self.posicoesMaisPossiveis[b][1]), len(self.posicoesMaisPossiveis[b][2]))
                                     for b in self.posicoesMaisPossiveis if b != 'neutros'}
                    print("-"*20)
                    print(maioresValores)
                    maiorValoresPossibilidade1 = sorted(maioresValores, key=lambda x: maioresValores[x][0])
                    print(maiorValoresPossibilidade1)
                    maiorValoresPossibilidade2 = sorted(maioresValores, key=lambda x: maioresValores[x][1])
                    print(maiorValoresPossibilidade2)
                    print("-"*20)

                    maiorValoresPossibilidade1 = sorted(maioresValores, key=lambda x: maioresValores[x][0])[-1]
                    maiorValoresPossibilidade2 = sorted(maioresValores, key=lambda x: maioresValores[x][1])[-1]
                    
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
                print(defesaOuAtaque, self.posicoesMaisPossiveis[defesaOuAtaque])
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
            if not botao: print('botao:', botao)
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
                botao.Disable() if botao in self.posicoesDisponiveis else None

        if isinstance(jogador, str):
            mensagem = "Parabéns, você ganhou o jogo!"
            self.pontuacaoUsuario += 1
        else:
            if jogador == 1:
                mensagem = "Que pena, " + self.nomeUsuario + " você se lascou!"
                self.pontuacaoPC += 1
            else:
                mensagem = "Deu velha!"

        textoMarkup = ("<span foreground='black'>Seja bem-vindo,</span> <b>{nome}</b>!\n"
                       "Placar atual é: {nome}={pontuacaoUsuario} x PC={pontuacaoPC}").format(
            nome=self.nomeUsuario,
            pontuacaoUsuario=self.pontuacaoUsuario,
            pontuacaoPC=self.pontuacaoPC)
        self.textoBemVindo.SetLabelMarkup(textoMarkup)
        
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
    janela = meuFrame(None, title="Jogo de velha", size=(500,500))
    app.MainLoop()

if __name__ == '__main__':
    main()
