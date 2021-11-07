import pyxel
from random import randint
from math import sqrt
from random import uniform

pyxel.init(256, 256,caption= "o jogo", fps = 30)
game_start = False
limpo = False

x=128
y=250
i=0
fase = 1
a = 2 
z = randint(a,2+fase)
radius = 10
teleporte = 1
tp_espada = 0
tp_teleporte = 0
ini_mov_speed = 1
cooldown_contador = 0
texto_cooldown = 0
restart = False
personagem_vivo = True
dev = False
proxima_fase = False
inimigo_vivo = []
lista_x_inimigo = []
lista_y_inimigo = []

for numero_inimigos in range (1,z):
    
    lista_x_inimigo.append(uniform(0,256))
    lista_y_inimigo.append(uniform(0,150))
    inimigo_vivo.append(True)

def update():
    global x,y,inimigo_vivo,personagem_vivo,cooldown_contador,numero_inimigos,game_start,lista_x_inimigo,lista_y_inimigo,dev,COR,limpo,fase,proxima_fase,z,a,ini_mov_speed,teleporte,restart,tp_espada,tp_teleporte
    if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    #menu
    if game_start == False :
        if pyxel.btnp(pyxel.KEY_ENTER):
            game_start = True 
        if pyxel.btnp(pyxel.KEY_D) and dev == False:
            dev = True
        elif pyxel.btnp(pyxel.KEY_D) and dev == True :
            dev = False
        if cooldown_contador == 0 :
            cooldown_contador = 30
            COR = randint(1,15)
        elif cooldown_contador > 0 :
            cooldown_contador -= 1

    if game_start == True :

        #mover personagem
        if personagem_vivo == True  :
            
            if pyxel.btn(pyxel.KEY_W) :
                if limpo == True or y - 3 > -1 :
                    y-=3
        
            if pyxel.btn(pyxel.KEY_S) and y + 3 < 257:
                y+=3
            if pyxel.btn(pyxel.KEY_D) and x + 3 <257:
                x+=3
            if pyxel.btn(pyxel.KEY_A) and x - 3 > -1:
                x-=3
        #inimigo se move ate vc

        for i in range (0,z-1) :
            if inimigo_vivo[i] == True and personagem_vivo == True and dev == False:
                
                if lista_x_inimigo[i]> x :
                    lista_x_inimigo[i]-=ini_mov_speed
                if lista_x_inimigo[i]< x :
                    lista_x_inimigo[i]+=ini_mov_speed
                if lista_y_inimigo[i]> y :
                    lista_y_inimigo[i]-=ini_mov_speed
                if lista_y_inimigo[i]< y :
                    lista_y_inimigo[i]+=ini_mov_speed 
        #colisão
                for j in range(i + 1, len(lista_x_inimigo)):
                    x1, y1 = lista_x_inimigo[i], lista_y_inimigo[i]
                    x2, y2 = lista_x_inimigo[j], lista_y_inimigo[j]
                    dx = x2 - x1
                    dy = y2 - y1
                    if sqrt(dx**2 + dy**2) < radius + radius:
                        lista_x_inimigo[i] = x1 - dx / 10
                        lista_y_inimigo[i] = y1 - dx / 10
                        lista_x_inimigo[j] = x2 + dx / 10
                        lista_y_inimigo[j] = y2 + dx / 10

        #ataque 
        
        if pyxel.btnp(pyxel.KEY_E) and cooldown_contador == 0 :
            cooldown_contador += 120
            tp_espada = 30
            for j in range (0,z-1) :
                if int(lista_x_inimigo[j]) - 10 in range (x-20,x+20) and int(lista_y_inimigo[j]) - 10 in range ( y-20,y+20) :
                    inimigo_vivo[j] = False
                if int(lista_x_inimigo[j]) + 10 in range (x-20,x+20) and int(lista_y_inimigo[j]) + 10 in range ( y-20,y+20) :
                    inimigo_vivo[j] = False


        elif cooldown_contador > 0 :
            cooldown_contador -= 1
            if tp_espada > 0 :
                tp_espada -= 1

        #teleporte 
        if pyxel.btnp(pyxel.KEY_SPACE) and teleporte == 1 and personagem_vivo == True:
            tp_teleporte = 30
            
            if dev == False :
                teleporte = 0 
            if x < 129 :
                if y < 129 :
                    x =256 
                    y =256
                else : 
                    x = 256
                    y = 0
            else :
                if y < 129 :
                    x = 0
                    y = 256
                else : 
                    x = 0 
                    y = 0
        if tp_teleporte > 0 :
            tp_teleporte -= 1

        #morte
        for k in range (0,z-1) :
            if inimigo_vivo[k] == True and dev == False:
                if x in range(int(lista_x_inimigo[k])-10,int(lista_x_inimigo[k])+10) and y in range(int(lista_y_inimigo[k])-10, int(lista_y_inimigo[k]) + 10) :
                    personagem_vivo = False 
        #proxima fase
        kills = 0
        for i in range (0,z-1) :
            if inimigo_vivo[i] == False :
                kills+=1
        if kills == len(lista_x_inimigo) :
            limpo = True 
        if y < 0 or restart == True:
            fase +=1
            teleporte = 1
            x=128
            y=250
            if fase > 1 or restart == True:
                if fase % 3 == 0 :
                    a += 2
                if fase % 2 == 0 :
                    ini_mov_speed += 0.2
                z = randint(a,2+fase)
                limpo = False
                inimigo_vivo = []
                lista_x_inimigo = []
                lista_y_inimigo = []
                for numero_inimigos in range (1,z):
                
                    lista_x_inimigo.append(uniform(0,256))
                    lista_y_inimigo.append(uniform(0,150))
                    inimigo_vivo.append(True)
            personagem_vivo = True
            restart = False
        #restart
        if personagem_vivo == False and pyxel.btnp(pyxel.KEY_R) :
            fase = 0
            a = 2
            ini_mov_speed = 1
            restart = True
            
       

def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    if game_start == False :
        pyxel.text (10, 10, "aperte enter para iniciar", pyxel.COLOR_WHITE)   
        pyxel.text (10, 20, "aperte D para ativar e desativar o modo desenvolvedor", pyxel.COLOR_WHITE)   
        pyxel.text (10, 30, "Dev: {0}".format(dev), pyxel.COLOR_WHITE)
        pyxel.text (10, 40, "TUTORIAL:", pyxel.COLOR_WHITE)   
        pyxel.text (20, 50, "Use WASD para se movimentar", pyxel.COLOR_WHITE)   
        pyxel.text (20, 60, "Use E para atacar", pyxel.COLOR_WHITE)  
        pyxel.text (20, 70, "Use SPACE para teleportar para uma area segura", pyxel.COLOR_WHITE)   
        pyxel.text (20, 80, "Use Q para fechar o aplicativo", pyxel.COLOR_WHITE)  
        pyxel.rectb(0, 192, 256, 64, 7)
        pyxel.text (10, 215, "TRABALHO FINAL DE APC", pyxel.COLOR_WHITE)
        pyxel.text (10, 230, "DESENVOLVEDOR: Christian Hirsch Santos", COR)
        
        

    if game_start == True :
       
        pyxel.cls(pyxel.COLOR_LIME)
        #estrada
        pyxel.rect(96, 0, 64, 256, 4)
        #personagem
        if personagem_vivo == True :
            frames = [1,13,37]
            i= (pyxel.frame_count // 10) % len(frames) 
            pyxel.blt(x-5,y-5,0,frames[i],1,10,10,0)
        

        #Criar imagem do inimigo
        for x_inimigo,y_inimigo in zip (lista_x_inimigo,lista_y_inimigo):
            
            pyxel.blt(x_inimigo-5,y_inimigo-5,0,1,13,20,20,0)
        
        pyxel.text (10, 0, "Fase: {0}".format(fase), pyxel.COLOR_BLACK)  
        pyxel.text (10, 10, "Teleportes: {0}".format(teleporte), pyxel.COLOR_BLACK) 

        #fim de jogo

        if personagem_vivo == False :
            pyxel.text (128, 128, "MORTO", pyxel.COLOR_BLACK)
            pyxel.text (128, 138, "Aperte R para recomecar", pyxel.COLOR_BLACK)


        if cooldown_contador > 0 :
            pyxel.text (10, 20, "Cooldown do ataque é: {:.1f}".format(cooldown_contador/30), pyxel.COLOR_BLACK)  
        
        #espada
        if tp_espada > 0 :
            pyxel.blt(x+5,y-5,0,49,1,10,10,2)

        #range de ataque
        if cooldown_contador == 0 :
            pyxel.circb(x, y, 20, 0) 
            
        if dev == True :
            pyxel.text (10, 30, "coordenadas: {0} {1}".format(x,y), pyxel.COLOR_BLACK)  
        if limpo == True or dev == True:
            pyxel.text (160, 5, "PROXIMA FASE LIBERADA", pyxel.COLOR_WHITE)
        #teleporte
        if tp_teleporte > 0 :
            pyxel.blt(x,y,0,49,12,10,10,0)
        #proxima fase
        if limpo == True :
            pyxel.blt(100,15,0,24,16,8,8,0)
            pyxel.blt(110,15,0,24,16,8,8,0)
            pyxel.blt(120,15,0,24,16,8,8,0)
            pyxel.blt(130,15,0,24,16,8,8,0)
            pyxel.blt(140,15,0,24,16,8,8,0)
            pyxel.blt(150,15,0,24,16,8,8,0)
        
        
pyxel.load("my_resource.pyxres")
pyxel.run(update, draw)
