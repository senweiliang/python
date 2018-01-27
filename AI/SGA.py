# 城市个数  
# 种群数量
# 迭代次数
# 重组概率 未重组的直接进入下一代 重组点数
# 突变概率 
# 87.0 路线: [3, 4, 2, 1, 0]
# 几个非常重要的注意点
# 1.python的函数中和全局同名的变量，如果有修改变量的值就会变成局部变量
# 如果确定要引用全局变量，并且要对它修改，必须加上global关键字
# 2.#random.randint和random.uniform两边都是闭区间
# 3.注意list为地址传递 不想影响原list需copy.copy 多维数组需要copy.deepcopy()
# 4.python 除法结果默认为浮点数 即使结果为整数
# 5.list.remove() 一次只能除去一个元素
# 6.距离较大时 精度也要比较大 否则适应度约等于0
import random
import copy
import math
INFINITY=9999
city=5
pop_size=10
generation=100
cross_p=0.8
mutate_p=0.1
city_dists=[[9999,25,41,32,28],[25,9999,18,31,26],[41,18,9999,7,1],[32.,31,7,9999,11],[28,26,1,11,9999]]
city_positions=[]
pop=[]
new_pop=[]
pop_dists=[]#记录相应解的距离值
fit=[]#记录倒数值
def getParent(pop,fit,fit_sum):
	rand=random.uniform(0, 1)
	sector_sum=0
	for k in range(pop_size):
		sector_sum+=fit[k]
		if (sector_sum/fit_sum)>rand:
			break
	return pop[k]
def crossOver(parent1,parent2):
	rand=random.uniform(0, 1)
	#不发生重组
	if rand>cross_p:
		return parent1,parent2
	#发生重组 进行交换
	start=random.randint(0,city-1)
	for i in range(start,city):
		temp=parent1[i]
		parent1[i]=parent2[i]
		parent2[i]=temp
	#去除除了交换部分以外重复的基因(城市)
	duplicate1=copy.copy(parent1)
	duplicate2=copy.copy(parent2)
	for i in range(city):
		try:
			duplicate1.remove(i)
			duplicate2.remove(i)
		except ValueError:
			pass

	length=len(duplicate1)
	for i in range(length):
		temp1=duplicate1[i]
		temp2=duplicate2[i]
		parent1[parent1.index(temp1)]=duplicate2[i]#由于.index方法从左至右扫描 返回遇到的第一个索引 因此不会影响交换的基因
		parent2[parent2.index(temp2)]=duplicate1[i]
	return parent1,parent2
def mutate(child):
	rand=random.uniform(0, 1)
	if rand>mutate_p:
		#不发生变异
		return child
	p1=random.randint(0, city-1)
	p2=random.randint(0, city-1)
	temp=child[p1]
	child[p1]=child[p2]
	child[p2]=temp
	return child
def calculate(pop_dists,fit,pop):
	fit_sum=0
	for i in range(pop_size):
		#计算每个解(个体)的距离
		sum_dist=city_dists[pop[i][0]][pop[i][-1]]
		for k in range(city-1):
			sum_dist+=city_dists[pop[i][k]][pop[i][k+1]]
		#计算适应度之和 每个个体的适应度
		pop_dists.append(sum_dist)
		
		single_fit=round(1/sum_dist,5)
		fit_sum+=single_fit
		fit.append(single_fit)
	return fit_sum
def init(pop):
	for i in range(pop_size):
		a=[i for i in range(city)]
		random.shuffle(a)
		pop.append(a)
def calCtDists(city_positions,city_dists):
	with open('input.txt','r') as f:
		for line in f.readlines():
			x,y=line.split(',')
			x=int(x)
			y=int(y)
			city_positions.append([x,y])
	length=len(city_positions)
	for i in range(city):
		city_dists.append([])
		for j in range(city):
			if i==j:
				city_dists[i].append(INFINITY)
				continue
			dx=city_positions[i][0]-city_positions[j][0]
			dy=city_positions[i][1]-city_positions[j][1]
			dist=round((math.sqrt(dx*dx+dy*dy)),5)
			city_dists[i].append(dist)

def main():

	global pop
	global new_pop
	global pop_dists
	global fit
	global city_dists
	global city_positions

	#calCtDists(city_positions, city_dists)

	#初始化种群
	init(pop)
	for g in range(generation):
		if g!=0:
			pop=copy.deepcopy(new_pop)
		new_pop=[]
		pop_dists=[]#记录相应解的距离值
		fit=[]#记录倒数值
		#fit_sum 存适应度(即距离倒数)之和
		fit_sum=calculate(pop_dists, fit,pop)
		#轮盘选择
		times=int(pop_size/2)#结果默认为浮点数
		for i in range(times):
			#选择父代
			parent1=copy.copy(getParent(pop,fit,fit_sum))
			parent2=copy.copy(getParent(pop,fit,fit_sum))
			#交叉互换
			child1,child2=copy.copy(crossOver(parent1,parent2))
			#变异
			child1=mutate(child1)
			child2=mutate(child2)
			new_pop.append(child1)
			new_pop.append(child2)
		if g%500==-1:
			print(g+1,"代新种群",new_pop)
	print("最后一代种群",new_pop)
	pop_dists=[]
	fit=[]
	calculate(pop_dists, fit,new_pop)
	min_dist=min(pop_dists)
	solution=new_pop[pop_dists.index((min_dist))]
	print("最短距离:",min_dist,"路线:",solution)
if __name__ == '__main__':
	main()



