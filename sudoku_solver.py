import copy
import pprint
import numpy as np
from queue import PriorityQueue
from random import shuffle
import gc

class Casilla:
  def __init__(self):
    self.value = 0
    self.amenazados = [1,2,3,4,5,6,7,8,9]
  
  def nuevo(self, valor):
    if(self.value==0):
      if(valor in self.amenazados):
        self.value=valor
        self.amenazados=[]
        return True
    return False

  def amenazar(self, value):
    if(value in self.amenazados):
      self.amenazados.remove(value)
      return True
    return False

class Tablero:
  def __init__(self, n):
    self.juego = np.array([[Casilla() for i in range(n*3)] for j in range(n*3)])
    self.tam=n

  def agregar_valor(self,value,i,j):
    if(self.juego[i][j].nuevo(value)):
      self.amenazar_cuadrante(value,i,j)
      self.amenazar_lateral(value,i)
      self.amenazar_horizontal(value,j)
      return True
    return False

  def amenazar_cuadrante(self,value,i,j):
    f_ii=0
    f_ij=0
    f_si=0
    f_sj=0
    piv_i=0
    piv_j=0
    for a in range(self.tam):
      for b in range(self.tam):
        lim_i=(a*3)+3
        lim_j=(b*3)+3
        if(i>=piv_i and i<=lim_i):
          if(j>=piv_j and j<=lim_j):
            f_ii=piv_i
            f_ij=piv_j
            f_si=lim_i
            f_sj=lim_j
        piv_j=lim_j
      piv_i=lim_i
    for a in range(f_ii,f_si):
      for b in range(f_ij, f_sj):
        self.juego[a][b].amenazar(value)


  def amenazar_lateral(self, value, i):
    for j in range(self.tam*3):
      self.juego[i][j].amenazar(value)
        

  def amenazar_horizontal(self, value, j):
    for i in range(self.tam*3):
      self.juego[i][j].amenazar(value)

  def retorna_matriz(self):
    m=np.zeros((self.tam*3,self.tam*3))
    for i in range(self.tam*3):
      for j in range(self.tam*3):
        m[i][j]=self.juego[i][j].value
    return m

  def consultar_ceros(self):
    m = self.retorna_matriz()
    n=np.count_nonzero(m)
    return n

class Sudoku:
  def __init__(self,n):
    self.value=0
    self.tam=n
    self.tablero = Tablero(n)

  def rellenar(self,valor,a,b):
    if(self.tablero.agregar_valor(valor,a,b)):
      self.value+=1
      return True
    return False

  def consultar(self):
    n=self.tablero.consultar_ceros()
    self.value=n
    return n

class State:
  def __init__(self, n):
    self.sudoku = Sudoku(n)
    self.final=(3*n)*(3*n)
    self.valor = 0

  def agregar(self,a,b,valor):
    if(self.sudoku.rellenar(valor,a,b)):
      self.valor -= 1
      return True
    return False
  
  def consulta(self):
    n=self.sudoku.consultar()
    self.valor = n
    return n

  def revisar(self):
    for i in range(self.sudoku.tam*3):
      for j in range(self.sudoku.tam*3):
        posibles=len(self.sudoku.tablero.juego[i][j].amenazados)
        if(posibles==0 and self.sudoku.tablero.juego[i][j].value==0):
          return True
    return False

class Action:
  def __init__(self,a,b,value,posibles):
    self.a=a
    self.b=b
    self.value=value
    self.posibles=posibles

def get_actions(s):
  actions=[]
  for a in range(s.sudoku.tam*3):
    for b in range(s.sudoku.tam*3):
      posibles=s.sudoku.tablero.juego[a][b].amenazados
      value=s.sudoku.tablero.juego[a][b].value
      cant=len(posibles)
      if(value==0 and cant!=0):
        for i in posibles:
          data=Action(a,b,i,cant)
          actions.append(data)
        return actions

def transition(s,action):
  s1=copy.deepcopy(s)
  a=action.a
  b=action.b
  valor=action.value
  s1.agregar(a,b,valor)
  print(s1.sudoku.tablero.retorna_matriz())
  return s1

def is_final_state(s):
  n=s.consulta()
  if (n == s.final) :
    return 1
  else:
    if(s.revisar()):
      return -1
  return 0

def bfs(s):
  q = PriorityQueue(0)
  count = 0
  contEstadoAgregados = 0
  q.put((s.valor, contEstadoAgregados, s))
  contEstadoAgregados += 1
  estadosFinales = []
  while not q.empty():
    s = q.get()
    piv=is_final_state(s[2])
    if piv==1:
      return s
      estadosFinales.append(s)
      count = count + 1
    elif piv==-1:
      del s 
      gc.collect()
      continue
    if count > 1:
      return 0
      #get_actions necesario
    actions = get_actions(s[2])
    for action in actions:
      #Transition necesidad
      nState = transition(s[2], action)
      #state.value necesidad ( valor para pushear en el arbol)
      contEstadoAgregados += 1
      q.put((nState.valor, contEstadoAgregados, nState))
  return estadosFinales