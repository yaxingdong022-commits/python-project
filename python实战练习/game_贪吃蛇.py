import random
import sys
from time import sleep
import pygame
width=600
height=600
screen=pygame.display.set_mode([width,height])
class snake():
    def __init__(self,screen):
        self.screen=screen
        self.body=[]
        self.fx=pygame.K_RIGHT
        self.init_body()
    def show_text(self,screen):
        word=pygame.font.SysFont("幼圆",60)
        word.set_bold(True)
        text=word.render('亖了',1,'red')
        tw=(width-text.get_width())//2
        th=(height-text.get_height())//2
        screen.blit(text,(tw,th))
        pygame.display.update()
    def init_body(self,length=5):
        left,top=(0,0)
        for i in range(length):
            if self.body:
                left,top=(self.body[0].left,self.body[0].top)
                #这个是↓调整蛇的身体 Rectangle
                node=pygame.Rect(left+20,top,20,20)
            else:
                node=pygame.Rect(0,0,20,20)
            self.body.insert(0,node)
    def draw(self):
        for n in self.body:
            pygame.draw.rect(self.screen,(62,122,178),n,0)
    def add_node(self):
        if self.body:
            left,top=(self.body[0].left,self.body[0].top)
            if self.fx==pygame.K_RIGHT:
                left+=20
            if self.fx==pygame.K_LEFT:
                left-=20
            if self.fx==pygame.K_UP:
                top-=20
            if self.fx==pygame.K_DOWN:
                top+=20
            node=pygame.Rect(left,top,20,20)
            self.body.insert(0,node)
    def del_node(self):
        self.body.pop()
    def move(self):
        self.del_node()
        self.add_node()
    def change(self,fx):
        LR=[pygame.K_LEFT,pygame.K_RIGHT]
        UD=[pygame.K_UP,pygame.K_DOWN]
        if fx in LR+UD:
            if fx in LR and self.fx in LR:
                return
            if fx in UD and self.fx in UD:
                return
            self.fx=fx
    def is_dead(self):
        if self.body[0].left not in range(width) or self.body[0].top not in range(height) or self.body[0] in self.body[1:]:#做一个列表的切片
            return True

class food():
    def __init__(self):
        # 从x方向的可选坐标中随机选一个left
        all_x_point = range(0, width - 20, 20)  # 步长20，确保和网格对齐
        left = random.choice(all_x_point)#这个是固定值可传入rect 但是range不能
        # 从y方向的可选坐标中随机选一个top
        all_y_point = range(0, height - 20, 20)
        top = random.choice(all_y_point)
        # 用具体的left和top创建Rect对象
        self.node = pygame.Rect(left, top, 20, 20)
        self.flag = False

    def set(self):
        all_x_point=range(0,width-20,20)
        all_y_point=range(0,height-20,20)
        left=random.choice(all_x_point)
        top=random.choice(all_y_point)
        self.node=pygame.Rect(left,top,20,20)


def main():
    pygame.init()


    sk=snake(screen)
    fd=food()
    while True:

        #遍历所有事件
        for event in pygame.event.get():
            #如果是退出事件就退出
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:#键按下去
                sk.change(event.key)#键传进去
        screen.fill((255,255,255))
        sk.draw()
        sk.move()
        if sk.is_dead():
            sleep(1)
            sk.show_text(sk.screen)
            sleep(5)
            sys.exit()
        pygame.draw.rect(screen, (62, 122, 178), fd.node, 0)
        if fd.flag:
            fd.set()
            fd.flag=False
        if sk.body[0]==fd.node:
            sk.add_node()
            fd.flag=True
        pygame.display.update()
        sleep(0.1)
if __name__ == '__main__':
    main()