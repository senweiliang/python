from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
import time
start=time.time()
img=np.array(Image.open('C:/Users/梁森维/Pictures/Screenshots/eagle.jpg'))#320*150 200*150的图像速度较快些
img_matrix=img.tolist()
img=np.array(img_matrix)
k=8# 10-30时间相对较快
rows,cols,dims=img.shape
means=[]#放中心点
clusters=[]
is_change=True
for i in range(k):
	clusters.append([])
	x=np.random.randint(0,rows)
	y=np.random.randint(0,cols)
	means.append(img_matrix[x][y])
print("初始化簇中心点:",means)
#for j in range(rows):
#	cluster_map.append([])
#	for k in range(cols):
#		cluster_map[j].append(-1)

while is_change:
	#初始化工作
	new_means=[]
	clusters=[]
	cluster_map=[]
	r,g,b=0,0,0
	is_change=False
	for i in range(k):
		clusters.append([means[i]])

	for p in range(rows):
		cluster_map.append([])
		for q in range(cols):
			
			c_index=0#假设当前点离第一个中心点最近
			min_dist=math.floor(math.sqrt((img_matrix[p][q][0]-means[0][0])**2 +(img_matrix[p][q][1]-means[0][1])**2+(img_matrix[p][q][2]-means[0][2])**2 ))
			for i in range(1,k):
				dist=math.floor(math.sqrt((img_matrix[p][q][0]-means[i][0])**2 +(img_matrix[p][q][1]-means[i][1])**2+(img_matrix[p][q][2]-means[i][2])**2 ))
				if dist<min_dist:
					min_dist=dist
					c_index=i
			clusters[c_index].append(img_matrix[p][q])#加到相应的簇里
			cluster_map[p].append(c_index)

	for c_index in range(k):
		r,g,b=0,0,0
		c_num=len(clusters[c_index])
		for i in range(c_num):
			r+=clusters[c_index][i][0]
			g+=clusters[c_index][i][1]
			b+=clusters[c_index][i][2]
		avg_r=math.floor(r/c_num)
		avg_g=math.floor(g/c_num)
		avg_b=math.floor(b/c_num)
		new_means.append([avg_r,avg_g,avg_b])
	#检查中心点是否有变化
	
	print(new_means)
	for i in range(k):
		if new_means[i] not in means:
			is_change=True
			means=new_means
			break
	time.sleep(1)
end=time.time()
print(end-start)
for p in range(rows):
        for q in range(cols):
                img_matrix[p][q][0]=255-means[cluster_map[p][q]][0]
                img_matrix[p][q][1]=255-means[cluster_map[p][q]][1]
                img_matrix[p][q][2]=255-means[cluster_map[p][q]][2]
# 可将上面循环换成下面代码
# 以下代码将图像分为side x side 大小的像素点 (R,G,B)取该区域聚类中心出现最多的为准 图像边界没有进行处理 没有优化处理 步骤较为繁琐
# side=3
# row_n=rows//side
# col_n=cols//side
# for p in range(row_n):
# 	for q in range(col_n):
# 		row_start=side*p
# 		row_end=side*(p+1)
# 		col_start=side*q
# 		col_end=side*(q+1)
# 		square=[]
# 		common_c=0
# 		for i in range(row_start,row_end):
# 			for j in range(col_start,col_end):
# 				square.append(cluster_map[i][j])
# 		np_square=np.array(square)
# 		common_c=np.argmax(np.bincount(np_square))
# 		for i in range(row_start,row_end):
# 			for j in range(col_start,col_end):
# 				img_matrix[i][j]=[255-means[common_c][0],255-means[common_c][1],255-means[common_c][2]]
img=np.array(img_matrix)

plt.figure("Aragaki")
plt.imshow(img)
plt.axis('off')
plt.show()
