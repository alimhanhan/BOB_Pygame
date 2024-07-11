import pygame
import random
import math
from pygame.locals import QUIT

class Star:
        def __init__(self, screen, screenSize, index):
                
                # 별의 사이즈는 기본적으로 1과 흰색
                self.size = 1
                self.color = (255, 255, 255)

                self.center = {
                        'x': screen.get_width() / 2,
                        'y': screen.get_height() / 2
                }
                self.radius = 0
                self.theta = 0

                # 화면의 사이즈는 매개변수로 받은 값을 그대로 사용
                self.screen = screen
                self.screenSize = screenSize

                self.init(index)

        # 어디까지 이동해야지 별이 끝까지 이동하는지를 파악하기 위한 함수
        # 별의 반지름 값이 해당 프로그램에서 최대 길이를 넘어갔을 때를 기준으로 끝까지 이동한 것으로 판단
        def getLimitDistance(self):
            return int(math.sqrt(math.pow(self.center['x'], 2)
                                    + math.pow(self.center['y'], 2)))
        
        
        # 색상 값은 랜덤함수를 이용하여 RGB값을 랜덤으로 변경
        def init(self, index):
            self.radius = float(random.randint(0, self.getLimitDistance()))
            self.color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
            )
            
            # 각도를 랜덤하게 한다면 별이 균등하지 않게 배포될 수 있기 때문에 하드코딩된 형태
            self.degree = (360 / 50) * index
            self.theta = float(self.degree) * math.pi / 180

        # 그림을 그려주는 함수
        # 메인 프로그램에서는 매번 프레임마다 반복문을 돌며 그림을 그리게 명령을 내림 -> 객체는 이 안에서 자신의 좌표 x, y를 구한다음 그림을 그리게 됨
        def draw(self, color):
            x = self.center['x'] + self.radius * math.cos(self.theta)
            y = self.center['y'] + self.radius * math.sin(self.theta)

            pygame.draw.circle(self.screen, color, [x, y], self.size)
        # 함수가 실행될 때마다 별의 반지름은 10%씩 증가하도록 설정됨 -> 별의 반지름이 커짐(멀어짐) 수록 빠르게 이동하여 운동시차 발생
        # 반지름 1은 초기값
        # 사이즈는 함수의 실행시마다 반지름의 1%만큼 커짐
        def move(self):
              self.radius += 1 + (float(self.radius) / 10)
              self.size = 1 + (self.radius / 100)
              self.draw(self.color)
            
                # 만약 별의 반지름이 최대값보다 커질 경우에는 별이 사라진 것이므로 다시 랜덤한 길이를 구하여 새로운 별로 출력
              if self.radius > self.getLimitDistance():
                    self.radius = float(random.randint(0, self.getLimitDistance()))


screenSize = {
      'width' : 1024,
      'height' : 768
}

# 초기 설정된 크기와 높이를 set_mode 메소드에 삽입하여 스크린 생성 
pygame.init()
screen = pygame.display.set_mode((screenSize['width'], screenSize['height']))
pygame.display.set_caption('Space Odyssey')

# main 함수가 실행되기 이전 별들의 목록 초기화(초기 0개)
stars = []

# 최대 별의 개수는 50개로 제한하여 별의 개수는 반복문이 실행되며 50개가 생성됨
# screen과 screenSize 매개변수는 하드코딩된 1024, 768이지만 index값은 0부터 49까지 증가함
for i in range(0, 50):
      star = Star(screen, screenSize, i)
      stars.append(star)

count = 0
delay = 10000
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    clock.tick(30)

    # 별의 잔상을 지워주기 위해 없애는 역할
    screen.fill((0, 0, 0))

    for star in stars:
         star.move()

    pygame.display.update()