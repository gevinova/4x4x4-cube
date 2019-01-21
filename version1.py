#version 1
#Tomando el cubo blanco arriba y verde al frente
import numpy as np
import random
#matrices por cara 
r=np.array([[5 for i in range(4)]for a in range (4)])
g=np.array([[2 for i in range(4)]for a in range (4)])
b=np.array([[4 for i in range(4)]for a in range (4)])
o=np.array([[6 for i in range(4)]for a in range (4)])
w=np.array([[1 for i in range(4)]for a in range (4)])
y=np.array([[3 for i in range(4)]for a in range (4)])


#funcion para rotar una matriz con parametros m(matriz a rotar) n(numero de veces)

def rotar(m,n):
    for j in range(n):
        resu=np.array(m)
        for i in range(4):
            for a in range(4):
                resu[i,a]=m[3-a,i]
        m=np.array(resu)
    return m

def conc(r,g,b,o,w,y):
    solh=np.hstack((w,g,y,b))
    solv1=np.hstack((r,rotar(r,1),rotar(r,2),rotar(r,3)))
    solv2=np.hstack((o,rotar(o,3),rotar(o,2),rotar(o,1)))
    #matriz solucion imagen
    sol=np.vstack((solv1,solh,solv2))
    return sol

def desconc(m):
    r=m[:4,:4]
    g=m[4:8,4:8]
    b=m[4:8,12:16]
    o=m[8:12,:4]
    w=m[4:8,:4]
    y=m[4:8,8:12]
    return r,g,b,o,w,y
# le  entra la matriz(m)  el movimiento (b) y el numero de movimientos(n)
def mov(m,b,n):
    
    m1=np.array(m)
    for i in range(n):
        #print("roto")
        #desconcatenar
        r0,g0,b0,o0,w0,y0=desconc(m1) 
        #u
        if (b=='U'):
            #rotamos la cara blanca
            w0=rotar(w0,1)
            #rotamos la cara roja para trabajar mas facil
            r1=rotar(r0,1)
            o1=rotar(o0,3)
            carry=np.array(r1[:,0])
            r1[:,0]=np.array(b0[:,3][::-1])#orden al revez 
            b0[:,3]=np.array(o1[:,0][::-1])
            o1[:,0]=np.array(g0[:,0])
            g0[:,0]=np.array(carry)
            m1 = np.array(conc(rotar(r1,3),g0,b0,rotar(o1,1),w0,y0))
        elif (b=='F'):
            m1[:,0:12]=m[:,4:16]
            m1[:,12:16]=m[:,:4]
            mf=mov(m1,'U',1)
            m1[:,:4]=mf[:,12:16]
            m1[:,4:16]=mf[:,:12]
        elif (b=='D'):
            m1[:,0:8]=m[:,8:16]
            m1[:,8:16]=m[:,:8]
            mf=mov(m1,'U',1)
            m1[:,:8]=mf[:,8:16]
            m1[:,8:16]=mf[:,:8]
        elif (b=='B'):
            m1[:,:4]=m[:,12:16]
            m1[:,4:16]=m[:,:12]
            mf=mov(m1,'U',1)
            m1[:,0:12]=mf[:,4:16]
            m1[:,12:16]=mf[:,:4]
        elif (b=='R'):
            r0=rotar(r0,1)
            carry=np.array(w0[0,:])
            w0[0,:]=g0[0,:]
            g0[0,:]=y0[0,:]
            y0[0,:]=b0[0,:]
            b0[0,:]=carry
            m1 = np.array(conc(r0,g0,b0,o0,w0,y0))
        elif (b=='L'):
            o0=rotar(o0,1)
            carry=np.array(w0[3,:])
            w0[3,:]=b0[3,:]
            b0[3,:]=y0[3,:]
            y0[3,:]=g0[3,:]
            g0[3,:]=carry
            m1 = np.array(conc(r0,g0,b0,o0,w0,y0))
        #movimientos intermedios
        elif (b=='u'): 
            #rotamos la cara roja para trabajar mas facil
            r1=rotar(r0,1)
            o1=rotar(o0,3)
            carry=np.array(r1[:,1])
            r1[:,1]=np.array(b0[:,2][::-1])#orden al revez 
            b0[:,2]=np.array(o1[:,1][::-1])
            o1[:,1]=np.array(g0[:,1])
            g0[:,1]=np.array(carry)
            m1 = np.array(conc(rotar(r1,3),g0,b0,rotar(o1,1),w0,y0))
        elif (b=='d'):
            m1[:,0:8]=m[:,8:16]
            m1[:,8:16]=m[:,:8]
            mf=mov(m1,'u',1)
            m1[:,:8]=mf[:,8:16]
            m1[:,8:16]=mf[:,:8]
        elif (b=='r'): #está en contra de las manecillas
            carry=np.array(w0[1,:])
            w0[1,:]=g0[1,:]
            g0[1,:]=y0[1,:]
            y0[1,:]=b0[1,:]
            b0[1,:]=carry
            m1 = np.array(conc(r0,g0,b0,o0,w0,y0))
        elif (b=='l'):
            carry=np.array(w0[2,:])
            w0[2,:]=b0[2,:]
            b0[2,:]=y0[2,:]
            y0[2,:]=g0[2,:]
            g0[2,:]=carry
            m1 = np.array(conc(r0,g0,b0,o0,w0,y0))
        elif (b=='f'):
            m1[:,0:12]=m[:,4:16]
            m1[:,12:16]=m[:,:4]
            mf=mov(m1,'u',1)
            m1[:,:4]=mf[:,12:16]
            m1[:,4:16]=mf[:,:12]
        elif (b=='b'):
            m1[:,:4]=m[:,12:16]
            m1[:,4:16]=m[:,:12]
            mf=mov(m1,'u',1)
            m1[:,0:12]=mf[:,4:16]
            m1[:,12:16]=mf[:,:4]
        #moviemientos w
        elif (b=='Uw'):
            #hacemos U
            mf=mov(m,'U',1)
            #luego u
            m1=mov(mf,'u',1)
        elif (b=='Dw'):
            #hacemos D
            mf=mov(m,'D',1)
            #luego d
            m1=mov(mf,'d',1)
        elif (b=='Rw'):
            #hacemos R
            mf=mov(m,'R',1)
            #luego r
            m1=mov(mf,'r',3)
        elif (b=='Lw'):
            #hacemos L
            mf=mov(m,'L',1)
            #luego l
            m1=mov(mf,'l',1)
        elif (b=='Bw'):
            #hacemos B
            mf=mov(m,'B',1)
            #luego b
            m1=mov(mf,'b',3)     
        elif (b=='Fw'):
            #hacemos B
            mf=mov(m,'F',1)
            #luego b
            m1=mov(mf,'f',1)    
        m=np.array(m1)  #se guarda en m el nuevo cubo, no quitar
    return m

#devuelvo una matriz de un cubo scrambleado con "n" movimientos distancia
def scramble(n,verbose=0):
    s=conc(r,g,b,o,w,y)
    for i in range(n):
        m,v= n_to_mov(random.randint(0,53))
        s=mov(s,m,v)  #ahora se hacen todos
        if verbose==1:
            print("scramble: "+str(m)+str(v))
    return s

def n_to_mov(n):        
    a="N"      #movimiento a realizar
    b=0         #numero de veces que se realiza ese movimiento "a"
    if (n==0): # U
        a='U'
        b=1
    elif (n==1): # F
        a='F'
        b=1
    elif (n==2): # D
        a='D'
        b=1
    elif (n==3): # B
        a='B'
        b=1
    elif (n==4): # R
        a='R'
        b=1
    elif (n==5): # L
        a='L'
        b=1
    elif (n==6): # U2
        a='U'
        b=2
    elif (n==7): # F2
        a='F'
        b=2
    elif (n==8): # D2
        a='D'
        b=2
    elif (n==9): # B2
        a='B'
        b=2
    elif (n==10): # R2
        a='R'
        b=2
    elif (n==11): # L2
        a='L'
        b=2
    elif (n==12): # U'
        a='U'
        b=3
    elif (n==13): # F'
        a='F'
        b=3
    elif (n==14): # D'
        a='D'
        b=3
    elif (n==15): # B'
        a='B'
        b=3
    elif (n==16): # R'
        a='R' 
        b=3
    elif (n==17): # L'
        a='L'
        b=3
    #movimientos de la mitad
    elif (n==18): # u
        a='u'
        b=1
    elif (n==19): # d
        a='d'
        b=1
    elif (n==20): # r
        a='r'
        b=1
    elif (n==21): # l
        a='l'
        b=1    
    elif (n==22): # f
        a='f'
        b=1
    elif (n==23): # b
        a='b'
        b=1
    elif (n==24): # u2
        a='u'
        b=2
    elif (n==25): # d2
        a='d'
        b=2
    elif (n==26): # r2
        a='r'
        b=2
    elif (n==27): # l2
        a='l'
        b=2    
    elif (n==28): # f2
        a='f'
        b=2
    elif (n==29): # b2
        a='b'
        b=2
    elif (n==30): # u'
        a='u'
        b=3
    elif (n==31): # d'
        a='d'
        b=3
    elif (n==32): # r'
        a='r'
        b=3
    elif (n==33): # l'
        a='l'
        b=3    
    elif (n==34): # f'
        a='f'
        b=3
    elif (n==35): # b'
        a='b'
        b=3
    #movimientos w
    elif (n==36): # Uw
        a='Uw'
        b=1
    elif (n==37): # Dw
        a='Dw'
        b=1
    elif (n==38): # Rw
        a='Rw'
        b=1
    elif (n==39): # Lw
        a='Lw'
        b=1
    elif (n==40): # Bw
        a='Bw'
        b=1
    elif (n==41): # Fw
        a='Fw'
        b=1
    elif (n==42): # Uw2
        a='Uw'
        b=2
    elif (n==43): # Dw2
        a='Dw'
        b=2
    elif (n==44): # Rw2
        a='Rw'
        b=2
    elif (n==45): # Lw2
        a='Lw'
        b=2
    elif (n==46): # Bw2
        a='Bw'
        b=2
    elif (n==47): # Fw2
        a='Fw'
        b=2
    elif (n==48): # Uw'
        a='Uw'
        b=3
    elif (n==49): # Dw'
        a='Dw'
        b=3
    elif (n==50): # Rw'
        a='Rw'
        b=3
    elif (n==51): # Lw'
        a='Lw'
        b=3
    elif (n==52): # Bw'
        a='Bw'
        b=3
    elif (n==53): # Fw'
        a='Fw'
        b=3
    return a,b
        
x=conc(r,g,b,o,w,y)
#xl=mov(x,'L',2)
#Uw r
#xs=mov(xl,'u',1)
'''x = mov(x,'U',1)
x = mov(x,'R',1)
x = mov(x,'R',3)
x = mov(x,'U',3)'''
#r1,g1,b1,o1,w1,y1=desconc(x)
#c1=conc(c[0],c[1],c[2],c[3],c[4],c[5])