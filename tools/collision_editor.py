#!/usr/bin/env python3
import sys, json
import pygame

try:
    import pyperclip
except ImportError:
    pyperclip=None

RADIUS=6

class Editor:
    def __init__(self,img):
        pygame.init()
        self.img=pygame.image.load(img)
        self.w,self.h=self.img.get_size()
        self.screen=pygame.display.set_mode((max(self.w,800),max(self.h,600)))
        self.img=self.img.convert_alpha()
        pygame.display.set_caption("Collision Editor")
        self.font=pygame.font.SysFont(None,22)
        self.origin=None
        self.points=[]
        self.drag=None

    def rel(self,p): return [p[0]-self.origin[0],p[1]-self.origin[1]]

    def export(self):
        data={"position":list(self.origin),"polygon":[self.rel(p) for p in self.points]}
        txt=json.dumps(data,indent=4)
        print(txt)
        if pyperclip:
            pyperclip.copy(txt)
            print("Copiado al portapapeles.")

    def point_at(self,pos):
        for i,p in enumerate(self.points):
            if (p[0]-pos[0])**2+(p[1]-pos[1])**2<RADIUS**2*4:
                return i
        return None

    def draw(self):
        self.screen.fill((40,40,40))
        self.screen.blit(self.img,(0,0))
        if self.origin:
            pygame.draw.line(self.screen,(0,255,0),(self.origin[0]-8,self.origin[1]),(self.origin[0]+8,self.origin[1]),2)
            pygame.draw.line(self.screen,(0,255,0),(self.origin[0],self.origin[1]-8),(self.origin[0],self.origin[1]+8),2)
        if len(self.points)>1:
            pygame.draw.lines(self.screen,(0,150,255),False,self.points,2)
            pygame.draw.line(self.screen,(0,150,255),self.points[-1],pygame.mouse.get_pos(),1)
        if len(self.points)>2:
            pygame.draw.line(self.screen,(0,150,255),self.points[-1],self.points[0],2)
        for p in self.points:
            pygame.draw.circle(self.screen,(255,0,0),p,RADIUS)
        txt=self.font.render("1º click: origen | Click: punto | Arrastrar: mover | Backspace: último | Supr: borrar | C: limpiar | Enter: exportar | Esc: salir",True,(255,255,255))
        self.screen.blit(txt,(5,5))
        pygame.display.flip()

    def run(self):
        clock=pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: return
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_ESCAPE:return
                    if e.key==pygame.K_RETURN and self.origin:self.export()
                    if e.key==pygame.K_BACKSPACE and self.points:self.points.pop()
                    if e.key==pygame.K_c:self.points=[];self.origin=None
                    if e.key==pygame.K_DELETE:
                        i=self.point_at(pygame.mouse.get_pos())
                        if i is not None:self.points.pop(i)
                if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                    if self.origin is None:self.origin=e.pos
                    else:
                        i=self.point_at(e.pos)
                        if i is None:self.points.append(e.pos)
                        else:self.drag=i
                if e.type==pygame.MOUSEBUTTONUP and e.button==1:self.drag=None
                if e.type==pygame.MOUSEMOTION and self.drag is not None:
                    self.points[self.drag]=e.pos
            self.draw();clock.tick(60)

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("Uso: python collision_editor.py imagen.png");raise SystemExit
    Editor(sys.argv[1]).run()
