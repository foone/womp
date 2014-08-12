#!/usr/bin/python
import pygame
from pygame.constants import *
import sys,os,re
from random import choice
from subprocess import Popen,PIPE
BG=(41,148,239)
SIZE=2
#open('/tmp/IWASHERE','wb').write('HEY')
if '--size' in sys.argv:
	SIZE=int(sys.argv[sys.argv.index('--size')+1])
def getScreenInfo(windowid):
	ret=Popen(['/usr/bin/xwininfo','-id',windowid],stdout=PIPE).communicate()[0]
	width=int(re.findall(r'Width: (\d+)',ret)[0])
	height=int(re.findall(r'Height: (\d+)',ret)[0])
	depth=int(re.findall('Depth: (\d+)',ret)[0])
	return width,height,depth
def draw():
	global lastpos
	if lastpos is None:
		screen.fill(BG)
		lastpos=(2*SIZE,2*SIZE)
		pygame.display.flip()
	x,y=lastpos
	updaterect=screen.blit(tiles,(x,y),choice(rects))
	x+=(22*SIZE)
	if x+(24*SIZE)>screen_size[0]:
		x=(2*SIZE)
		y+=(22*SIZE)
		if y+(24*SIZE)>screen_size[1]:
			y=(2*SIZE)
	blackrect=(x,y,20*SIZE,20*SIZE)
	blackrect=screen.blit(nexttile,(x,y))
	pygame.display.update([updaterect,blackrect])
		
	lastpos=(x,y)
def update():
	pass
def init():
	global screen,screen_size,buffer,tiles,lastpos,nexttile
	flags=DOUBLEBUF
	depth=0
	if '--root' in sys.argv or '-root' in sys.argv:
		windowid=os.environ.get('XSCREENSAVER_WINDOW')
		if windowid is None:
			sys.exit('Need XSCREENSAVER_WINDOW!')
		w,h,depth=getScreenInfo(windowid)
		os.environ['SDL_WINDOWID']=windowid
		screen_size=(w,h)
		flags=0
	else:
		screen_size=(640,480)
		if '-f' in sys.argv or '--fullscreen' in sys.argv:
			flags|=FULLSCREEN
	pygame.init()
	pygame.display.set_caption('Womp')
	screen=pygame.display.set_mode(screen_size,flags,depth)
	tiles=pygame.image.load('/home/foone/Desktop/py/screensaver/BIG2.png').convert()
	nexttile=pygame.image.load('/home/foone/Desktop/py/screensaver/next.png').convert()
	if SIZE!=1:
		tiles=resize(tiles)
		nexttile=resize(nexttile)
	pygame.mouse.set_visible(False)
	generateRects()
	lastpos=None
def generateRects():
	global rects
	rects=[]
	for i in range(22):
		rects.append(rectscale((2+21*i,2,20,20)))
		rects.append(rectscale((2+21*i,23,20,20)))
def rectscale(r):
	if SIZE==1:
		return r
	else:
		r=pygame.Rect(r)
		r.left*=SIZE
		r.top*=SIZE
		r.width*=SIZE
		r.height*=SIZE
		return r
def resize(surf):
	w,h=surf.get_size()
	return pygame.transform.scale(surf,(w*SIZE,h*SIZE))
def main():
	global running,lastpos
	init()
	drawing=running=True
	while running:
		pygame.time.wait(5)
		if drawing:
			draw()
		for event in pygame.event.get():
			if event.type==QUIT:
				running=False
				quit()
			elif event.type ==KEYUP:
				if event.key==K_ESCAPE:
					running=False
				if event.key==K_d:
					drawing=not drawing
	pygame.quit()
if __name__=='__main__':
	main()
