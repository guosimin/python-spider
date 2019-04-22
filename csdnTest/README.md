### 技术栈：  
* ui框架：element-ui框架

* 前端框架：vue-cli

* 后端框架：koa

* 前、后语言：javascript

* 爬虫语言：python

### 前后端代码（需要可视化的视图的时启动）   

https://github.com/guosimin/data-management 

1.下载代码，并启动并构建前端项目     
```
# install dependencies

npm install

# serve with hot reload at localhost:8080

npm run dev
```
2.打开另外一个命令行窗口，启用后端服务   

```
node app.js
```
3.启动完成后访问：http://localhost:8081/#/charts   

### 可视化的视图展示效果：   
![](https://img-blog.csdnimg.cn/20190402144205489.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)




### 爬虫代码(定时执行)  
https://github.com/guosimin/python-spider/tree/master/csdnTest/csdn-test.py

1.创建基本任务  
![](https://img-blog.csdnimg.cn/20190402145210482.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)

2.命名  
![](https://img-blog.csdnimg.cn/20190402145323316.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)


3.定义执行时间   
![](https://img-blog.csdnimg.cn/20190402145404548.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)

![](https://img-blog.csdnimg.cn/20190402145424196.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)

![](https://img-blog.csdnimg.cn/20190402145441390.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)


4.先看看我们的python装在哪个目录了   
![](https://img-blog.csdnimg.cn/20190402145714922.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)


5.然后按下图填写   
![](https://img-blog.csdnimg.cn/20190402150322174.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)


6.* **这也是最需要注意的**（在pyCharm执行成功的，在定时任务中却不一定成功，原因是python程序中使用 import XXX 时，python解析器会在当前目录、已安装和第三方模块中搜索 xxx，如果都搜索不到就会报错。我的项目引用了../model里面的模块，所以此时我需要用sys.path.append临时添加搜索路径，方便更简洁的import其他包和模块）   

```python
import sys
sys.path.append(r'E:\projects\python-spider')
```
7.执行(可以点击运行，如果结果为0*1则代码执行失败，如果为0*0则代码执行成功)  

![](https://img-blog.csdnimg.cn/20190402151156153.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2dpdGh1Yl8zOTU3MDcxNw==,size_16,color_FFFFFF,t_70)



### last UPdate          
* 20190417       
1.读取csdn_user表用户，来进行爬取     
2.调整爬取的并发数量     
3.新增获取一定数量用户的方法getUser.py,需要直接run执行，**建议限制爬取数量**,否则时间可能太长。
该方法获通过调用csdn的接口获取数据，但是当超过一定数量后，获取的数据则是重复的随机。有兴趣的注意观察