# python学习之美多商城(十二):商品部分:Docker使用(安装与操作)

## 一、Docker使用

### 1.什么是Docker

#### 1.1 容器技术
在计算机的世界中, 容器拥有一段漫长且传奇的历史。容器与管理程序虚拟化 (hypervisor virtualization，HV)有所不同，管理程序虚拟化通过中间层将一台或者多台独立 的机器虚拟运行与物理硬件之上，而容器则是直接运行在操作系统内核之上的用户空间。因 此，容器虚拟化也被称为“操作系统级虚拟化”，容器技术可以让多个独立的用户空间运行 在同一台宿主机上。

由于“客居”于操作系统，容器只能运行与底层宿主机相同或者相似的操作系统，这看 起来并不是非常灵活。例如:可以在 Ubuntu 服务中运行 Redhat Enterprise Linux，但无法再 Ubuntu 服务器上运行 Microsoft Windows。

相对于彻底隔离的管理程序虚拟化，容器被认为是不安全的。而反对这一观点的人则认 为，由于虚拟容器所虚拟的是一个完整的操作系统，这无疑增大了攻击范围，而且还要考虑 管理程序层潜在的暴露风险。

尽管有诸多局限性，容器还是被广泛部署于各种各样的应用场合。在超大规模的多租户 服务部署、轻量级沙盒以及对安全要求不太高的隔离环境中，容器技术非常流行。最常见的 一个例子就是“权限隔离监牢”(chroot jail)，它创建一个隔离的目录环境来运行进程。 如果权限隔离监牢正在运行的进程被入侵者攻破，入侵者便会发现自己“身陷囹圄”，因为 权限不足被困在容器所创建的目录中，无法对宿主机进一步破坏。

最新的容器技术引入了 OpenVZ、Solaris Zones 以及 Linux 容器(LXC)。使用这些新技 术，容器不在仅仅是一个单纯的运行环境。在自己的权限类内，容器更像是一个完整的宿主 机。对 Docker 来说，它得益于现代 Linux 特性，如控件组(control group)、命名空间 (namespace)技术，容器和宿主机之间的隔离更加彻底，容器有独立的网络和存储栈，还 拥有自己的资源管理能力，使得同一台宿主机中的多个容器可以友好的共存。

容器被认为是精益技术，因为容器需要的开销有限。和传统虚拟化以及半虚拟化相比， 容器不需要模拟层(emulation layer)和管理层(hypervisor layer)，而是使用操作系统的系 统调用接口。这降低了运行单个容器所需的开销，也使得宿主机中可以运行更多的容器。

尽管有着光辉的历史，容器仍未得到广泛的认可。一个很重要的原因就是容器技术的复 杂性:容器本身就比较复杂，不易安装，管理和自动化也很困难。而 Docker 就是为了改变 这一切而生的。

#### 1.2 容器与虚拟机的比较

1）本质上的区别：

![1561350518432](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561350518432.png)



2）使用上的区别：

![1561350588077](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561350588077.png)



#### 1.3 Docker特点

1) 上手快

用户只需要几分钟，就可以把自己的程序“Docker 化”。Docker 依赖于“写时复制” (copy-on-write)模型，使修改应用程序也非常迅速，可以说达到“随心所致，代码即改” 的境界。

随后，就可以创建容器来运行应用程序了。大多数 Docker 容器只需要不到 1 秒中即可 启动。由于去除了管理程序的开销，Docker 容器拥有很高的性能，同时同一台宿主机中也 可以运行更多的容器，使用户尽可能的充分利用系统资源。

2） 职责的逻辑分类

使用 Docker，开发人员只需要关心容器中运行的应用程序，而运维人员只需要关心如 何管理容器。Docker 设计的目的就是要加强开发人员写代码的开发环境与应用程序要部署 的生产环境一致性。从而降低那种“开发时一切正常，肯定是运维的问题(测试环境都是正 常的，上线后出了问题就归结为肯定是运维的问题)”

3） 快速高效的开发生命周期

Docker 的目标之一就是缩短代码从开发、测试到部署、上线运行的周期，让你的应用 程序具备可移植性，易于构建，并易于协作。(通俗一点说，Docker 就像一个盒子，里面 可以装很多物件，如果需要这些物件的可以直接将该大盒子拿走，而不需要从该盒子中一件 件的取。)

4） 鼓励使用面向服务的架构

Docker 还鼓励面向服务的体系结构和微服务架构。Docker 推荐单个容器只运行一个应 用程序或进程，这样就形成了一个分布式的应用程序模型，在这种模型下，应用程序或者服 务都可以表示为一系列内部互联的容器，从而使分布式部署应用程序，扩展或调试应用程序 都变得非常简单，同时也提高了程序的内省性。(当然，可以在一个容器中运行多个应用程 序)

### 2. Docker组件

#### 2.1 Docker客户端和服务器

Docker 是一个客户端-服务器(C/S)架构程序。Docker 客户端只需要向 Docker 服务器 或者守护进程发出请求，服务器或者守护进程将完成所有工作并返回结果。Docker 提供了 一个命令行工具 Docker 以及一整套 RESTful API。你可以在同一台宿主机上运行 Docker 守护 进程和客户端，也可以从本地的 Docker 客户端连接到运行在另一台宿主机上的远程 Docker 守护进程。

![1561350839968](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561350839968.png)



#### 2.2 Docker镜像
镜像是构建 Docker 的基石。用户基于镜像来运行自己的容器。镜像也是 Docker 生命周 期中的“构建”部分。镜像是基于联合文件系统的一种层式结构，由一系列指令一步一步构 建出来。例如:

添加一个文件;

执行一个命令;

打开一个窗口。

也可以将镜像当作容器的“源代码”。镜像体积很小，非常“便携”，易于分享、存储和更 新。

#### 2.3 Registry（注册中心）
Docker 用 Registry 来保存用户构建的镜像。Registry 分为公共和私有两种。Docker 公司 运营公共的 Registry 叫做 Docker Hub。用户可以在 Docker Hub 注册账号，分享并保存自己的 镜像(说明:在 Docker Hub 下载镜像巨慢，可以自己构建私有的 Registry)。

#### 2.4 Docker容器

Docker 可以帮助你构建和部署容器，你只需要把自己的应用程序或者服务打包放进容 器即可。容器是基于镜像启动起来的，容器中可以运行一个或多个进程。我们可以认为，镜 像是Docker生命周期中的构建或者打包阶段，而容器则是启动或者执行阶段。 容器基于 镜像启动，一旦容器启动完成后，我们就可以登录到容器中安装自己需要的软件或者服务。

![1561351211734](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561351211734.png)

所以 Docker 容器就是: 一个镜像格式; 一些列标准操作; 一个执行环境。

Docker 借鉴了标准集装箱的概念。标准集装箱将货物运往世界各地，Docker 将这个模 型运用到自己的设计中，唯一不同的是:集装箱运输货物，而 Docker 运输软件。

和集装箱一样，Docker 在执行上述操作时，并不关心容器中到底装了什么，它不管是 web 服务器，还是数据库，或者是应用程序服务器什么的。所有的容器都按照相同的方式将 内容“装载”进去。

Docker 也不关心你要把容器运到何方:我们可以在自己的笔记本中构建容器，上传到 Registry，然后下载到一个物理的或者虚拟的服务器来测试，在把容器部署到具体的主机中。 像标准集装箱一样，Docker 容器方便替换，可以叠加，易于分发，并且尽量通用。

使用 Docker，我们可以快速的构建一个应用程序服务器、一个消息总线、一套实用工 具、一个持续集成(CI)测试环境或者任意一种应用程序、服务或工具。我们可以在本地构 建一个完整的测试环境，也可以为生产或开发快速复制一套复杂的应用程序栈。

### 3. 使用Docker做什么
容器提供了隔离性，结论是，容器可以为各种测试提供很好的沙盒环境。并且，容器本

身就具有“标准性”的特征，非常适合为服务创建构建块。Docker 的一些应用场景如下:

加速本地开发和构建流程，使其更加高效、更加轻量化。本地开发人员可以构建、 运行并分享 Docker 容器。容器可以在开发环境中构建，然后轻松的提交到测试环境中，并 最终进入生产环境。
能够让独立的服务或应用程序在不同的环境中，得到相同的运行结果。这一点在 面向服务的架构和重度依赖微型服务的部署由其实用。
用 Docker 创建隔离的环境来进行测试。例如，用 Jenkins CI 这样的持续集成工具 启动一个用于测试的容器。

Docker 可以让开发者先在本机上构建一个复杂的程序或架构来进行测试，而不是 一开始就在生产环境部署、测试。

### 4. 在Ubuntu中安装Docker

可参考docker官网<https://docs.docker.com/install/linux/docker-ce/ubuntu/>

此处我们在Linux中安装

* 系统要求

  > Docker 要求 Ubuntu 系统的内核版本高于 3.10 ，查看本页面的前提条件来验证你的 Ubuntu 版本是否支持 Docker。
  >
  > 通过`uname -r`查看当前内核版本
  >
  > ~~~
  > root@qmpython:~# uname -r
  > 4.4.0-117-generic
  > ~~~

* 卸载/移除旧版本

  > 由于apt官方库里的docker版本可能比较旧，所以先卸载可能存在的旧版本：
  >
  > ~~~python
  > $ sudo apt-get remove docker docker-engine docker.io containerd runc
  > ~~~

* 更新apt包索引

  > ~~~
  > $ sudo apt-get update
  > ~~~

* 安装以下包以使apt可以通过HTTPS使用存储库（repository）

  > $ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

* 添加Docker官方的GPG密钥

  > ```
  > $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  > ```

* 使用下面的命令来设置**stable**存储库

  > $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

* 再更新一下apt包索引

  > ```
  > sudo apt-get update
  > ```

* 安装最新版本的Docker CE

  > ```
  > $ sudo apt-get install docker-ce docker-ce-cli containerd.io
  > ```

- 在生产系统上，可能会需要应该安装一个特定版本的Docker CE，而不是总是使用最新版本

  > 列出可用的版本：
  >
  > ```
  > $ apt-cache madison docker-ce
  > ```
  >
  > 选择要安装的特定版本，第二列是版本字符串，第三列是存储库名称，它指示包来自哪个存储库，以及扩展它的稳定性级别。要安装一个特定的版本，将版本字符串附加到包名中，并通过等号(=)分隔它们：
  >
  > ```
  > $ sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
  > ```

### 5. 验证docker

安装完成后，我们需要验证是否安装正确，可以通过运行 `hello-world` image。

~~~
$ sudo docker run hello-world
~~~

![1561353147133](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561353147133.png)

则说明成功。



### 6. 启动与停止

安装完成Docker后,默认已启动了docker服务,如需手动控制docker服务的启停,可执行如下命令

~~~
# 启动docker
sudo service docker start
# 停止docker
sudo service docker stop
# 重启docker
sudo service docker restart
~~~



## 二、Docker镜像

### 1. 什么是Docker镜像

Docker 镜像是由文件系统叠加而成(是一种文件的存储形式)。最底端是一个文件引 导系统，即 bootfs，这很像典型的 Linux/Unix 的引导文件系统。Docker 用户几乎永远不会和 引导系统有什么交互。实际上，当一个容器启动后，它将会被移动到内存中，而引导文件系 统则会被卸载，以留出更多的内存供磁盘镜像使用。Docker 容器启动是需要一些文件的， 而这些文件就可以称为 Docker 镜像。

![1561356449341](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561356449341.png)

Docker 把应用程序及其依赖，打包在 image 文件里面。 只有通过这个文件，才能生成 Docker 容器。image 文件可以看作是容器的模板。Docker 根据 image 文件生成容器的实例。同一个 image 文件，可以生成多个同时运行的容器实例。

image 是二进制文件。实际开发中，一个 image 文件往往通过继承另一个 image 文件，加上一些个性化设置而生成。举例来说，你可以在 Ubuntu 的 image 基础上，往里面加入 Apache 服务器，形成你的 image。

image 文件是通用的，一台机器的 image 文件拷贝到另一台机器，照样可以使用。一般来说，为了节省时间，我们应该尽量使用别人制作好的 image 文件，而不是自己制作。即使要定制，也应该基于别人的 image 文件进行加工，而不是从零开始制作。

为了方便共享，image 文件制作完成后，可以上传到网上的仓库。Docker 的官方仓库 Docker Hub 是最重要、最常用的 image 仓库。此外，出售自己制作的 image 文件也是可以的。

* 列出所有镜像文件：

  ~~~
  sudo docker image ls
  或
  sudo docker images -a
  ~~~

  ![1561356620337](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561356620337.png)

> - REPOSITORY：镜像所在的仓库名称
>
> - TAG：镜像标签
> - IMAGEID：镜像ID
> - CREATED：镜像的创建日期(不是获取该镜像的日期)
> - SIZE：镜像大小

为了区分同一个仓库下的不同镜像，Docker 提供了一种称为标签(Tag)的功能。每个 镜像在列出来时都带有一个标签，例如latest、 12.10、12.04 等等。每个标签对组成特定镜像的一 些镜像层进行标记(比如，标签 12.04 就是对所有 Ubuntu12.04 镜像层的标记)。这种机制 使得同一个仓库中可以存储多个镜像。— 版本号

我们在运行同一个仓库中的不同镜像时，可以通过在仓库名后面加上一个冒号和标签名 来指定该仓库中的某一具体的镜像，例如 docker run --name custom_container_name –i –t docker.io/ubunto:12.04 /bin/bash，表明从镜像 Ubuntu:12.04 启动一个容器，而这个镜像的操 作系统就是 Ubuntu:12.04。在构建容器时指定仓库的标签也是一个好习惯。

* 拉取镜像文件

  Docker维护了镜像仓库，分为共有和私有两种，共有的官方仓库Docker Hub(https://hub.docker.com/)是最重要最常用的镜像仓库。私有仓库（Private Registry）是开发者或者企业自建的镜像存储库，通常用来保存企业 内部的 Docker 镜像，用于内部开发流程和产品的发布、版本控制。要想获取某个镜像，我们可以使用pull命令，从仓库中拉取镜像到本地，如

  ~~~
  sudo docker image pull library/hello-world
  ~~~

  上面代码中，docker image pull是抓取 image 文件的命令。library/hello-world是 image 文件在仓库里面的位置，其中library是 image 文件所在的组，hello-world是 image 文件的名字。

  由于 Docker 官方提供的 image 文件，都放在library组里面，所以它的是默认组，可以省略。因此，上面的命令可以写成下面这样。

  ~~~
  sudo docker image pull hello-world
  ~~~

* 删除镜像

  ~~~
  sudo docker image rm 镜像名或镜像id
  或
  sudo docker rmi 镜像id
  ~~~

## 三、Docker容器操作

### 1. 创建容器

~~~
sudo docker run [option] 镜像名 [向启动容器中传入的命令]
~~~

> 常用可选参数说明：
>
> * -i 表示以“交互模式”运行容器；
> * -t 表示容器启动后会进入其命令行。加入这两个参数后，容器创建就能登录进去。即 分配一个伪终端；
> * –name 为创建的容器命名；
> * -v 表示目录映射关系(前者是宿主机目录，后者是映射到宿主机上的目录，即 宿主机目录:容器中目录)，可以使 用多个-v 做多个目录或文件映射。注意:最好做目录映射，在宿主机上做修改，然后 共享到容器上；
> * -d 在run后面加上-d参数,则会创建一个守护式容器在后台运行(这样创建容器后不 会自动登录容器，如果只加-i -t 两个参数，创建后就会自动进去容器)；
> * -p 表示端口映射，前者是宿主机端口，后者是容器内的映射端口。可以使用多个-p 做多个端口映射；
> * -e 为容器设置环境变量；
> * –network=host 表示将主机的网络环境映射到容器中，容器的网络与主机相同。

### 2. 交互式容器

例如, 创建一个交互式容器, 并命名为myubuntu

~~~
sudo docker run -it --name=myubuntu ubuntu /bin/bash
~~~

在容器中可以随意执行linux命令,就是一个ubuntu的环境,当执行exit命令退出时, 该容器也随之停止。

### 3. 守护式容器

创建一个守护式容器: 如果对于一个需要长期运行的容器来说,我们可以创建一个守护石容器。在容器内部exit退出时,容器不会停止。

~~~
sudo docker run -dit --name=myubuntu2 ubuntu
~~~

### 4. 进入已运行的容器

~~~
sudo docker exec -it 容器名或容器id 进入后执行的第一个命令
例如：
sudo docker exec -it myubuntu2 /bin/bash
~~~

### 5. 查看容器

~~~
# 查看正在运行的容器
sudo docker container ls
或
sudo docker ps

# 查看所有的容器,包括已停止运行的容器
sudo docker container ls --all
或
sudo docker ps -a
~~~

### 6. 停止与启动容器

~~~
# 停止一个已经在运行的容器
sudo docker container stop 容器名或容器id

# 启动一个已经停止的容器
sudo docker container start 容器名或容器id

# kill掉一个已经在运行的容器
sudo docker container kill 容器名或容器id

~~~

### 7. 删除容器

~~~
sudo docker rm 容器名或容器ID
~~~

### 8. 将容器保存为镜像

~~~
sudo docker commit 容器名 镜像名
~~~

### 9. 镜像备份与迁移

~~~
sudo docker save -o 保存的文件名 镜像名
例如：
sudo docker save -o ./ubuntu.tar ubuntu
~~~

在拿到镜像文件后，可以通过load方法，将镜像加载到本地

~~~
sudo docker load -i ./ubuntu.tar
~~~





# python学习之美多商城(十三):商品部分:FastDFS、Docker安装FastDFS、FastDFS客户端与自定义文件存储系统

## 一、什么是FastDFS

FastDFS 是用 c 语言编写的一款开源的分布式文件系统。FastDFS 为互联网量身定制， 充分考虑了冗余备份、负载均衡、线性扩容等机制，并注重高可用、高性能等指标，使用 FastDFS 很容易搭建一套高性能的文件服务器集群提供文件上传、下载等服务。主要解决了海量数据存储问题，特别适合以中小文件（建议范围：4KB < file_size <500MB）为载体的在线服务。 

FastDFS 系统有三个角色：**跟踪服务器(Tracker Server)**、**存储服务器(Storage Server)**和**客户端(Client)**。 

客户端请求Tracker server进行文件上传、下载，通过Tracker server调度最终由Storage server完成文件上传、下载。

* Tracker server 作用是负载均衡和调度，通过Tracker server在文件上传时可以根据一些策略找到Storage server提供文件上传服务。可以将tracker称为追踪服务器或调度服务器。负责管理所有的 storage server和 group，每个 storage 在启动后会连接 Tracker，告知自己所属 group 等信息，并保持周期性心跳。 
* Storage server作用是文件存储，客户端上传的文件最终存储在Storage服务器上，Storage server没有实现自己的文件系统，而是利用操作系统的文件系统来管理文件。可以将storage称为存储服务器。以 group 为单位，每个 group 内可以有多台 storage server，数据互为备份。 
* Client：客户端，上传下载数据的服务器，也就是我们自己的项目所部署在的服务器。

![1561431060276](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561431060276.png)



## 二、文件上传流程:

![1561432722715](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561432722715.png)



FastDFS向使用者提供基本文件访问接口，比如upload、download、append、delete等，以客户端库的方式提供给用户使用。 
Storage Server会定期的向Tracker Server发送自己的存储信息。当Tracker Server Cluster中的Tracker Server不止一个时，各个Tracker之间的关系是对等的，所以客户端上传时可以选择任意一个Tracker。 

当Tracker收到客户端上传文件的请求时，会为该文件分配一个可以存储文件的group，当选定了group后就要决定给客户端分配group中的哪一个storage server。当分配好storage server后，客户端向storage发送写文件请求，storage将会为文件分配一个数据存储目录。然后为文件分配一个fileid，最后根据以上的信息生成文件名存储文件。

客户端上传文件后存储服务器将文件ID返回给客户端,此文件ID用于访问文件的索引信息。文件索引信息包括:组名, 虚拟磁盘路径， 数据两级目录，文件名。

![1561432926881](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561432926881.png)

组名 : 文件上传后所在的storage组名称, 在文件上传成功后有storage服务器返回,需要客户端自行保存。
虚拟磁盘路径 : storage配置;额虚拟路径, 与磁盘选项store_path*对应。如果配置了store_path0则是M00, 如果配置了store_path1则是M哦, 以此类推。
数据两级目录 ：storage 服务器在每个虚拟磁盘路径下创建的两级目录，用于存储数据 文件。

文件名 ：与文件上传时不同。是由存储服务器根据特定信息生成，文件名包含:源存储 服务器 IP 地址、文件创建时间戳、文件大小、随机数和文件拓展名等信息。

## 三、简易FastDFS构建:

![1561433192841](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561433192841.png)



## 四、Docker安装FastDFS

### 1. 镜像下载：

可以利用已有的FastDFS Docker镜像来运行Fast DFS。

~~~
docker image pull delron/fastdfs
~~~

### 2. 运行tracker

~~~
sudo docker run -dti --network=host --name tracker -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker
~~~

> 我们将fastDFS tracker运行目录映射到本机的 /var/fdfs/tracker目录中。

* 查看tracker是否运行起来

~~~
docker container ls
~~~

![1559920312355](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1559920312355.png)

> status一列为UP则是运行了。

* 如果想停止tracker服务

  ~~~
  docker container stop tracker
  ~~~

  

* 停止后，重新运行tracker

  ~~~
  sudo docker container start tracker
  ~~~

  

### 3. 运行storage

开启storage服务：

```python
sudo docker run -dti --network=host --name storage -e TRACKER_SERVER=172.18.140.24:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
```

> TRACKER_SERVER=本机的IP地址：22122 本机的ip地址不要使用127.0.0.1。
>
> 通过在Ubuntu里面`ifconfig`查看本机IP地址：
>
> ![1559921079314](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1559921079314.png)
>
> 我们将fastDFS storage运行目录映射到本机的/var/fdfs/storage目录。

* 查看storage是否运行起来

  ~~~
  sudo docker container ps
  ~~~

* 停止storage服务

  ~~~
  sudo docker container stop storage
  ~~~

* 重新运行storage

  ~~~
  sudo docker container start storage
  ~~~

**注意：如果无法重新运行，可以删除/var/fdfs/storage/data目录下的fdfs_storaged.pid 文件，然后重新运行storage。**



## 五、FastDFS客户端与自定义文件存储系统

### 1. FastDFS的python客户端

python版本的FastDFS客户端使用说明参考:<https://github.com/jefforeilly/fdfs_client-py>

#### 1.1 安装

安装提供的`fdfs_client-py-master.zip`文件到虚拟环境中

1）进入虚拟环境；

2）进入`fdfs_client-py-master.zip`所在目录；

3) 执行命令安装

~~~
pip install fdfs_client-py-master.zip

pip install mutagen
pip isntall requests
~~~

#### 1.2 使用

使用FastDFS客户端，需要有配置文件。我们在meiduo_mall/utils目录下新建fastdfs目录，将提供的client.conf配置文件放到这个目录中。需要修改一下client.conf配置文件

~~~
connect_timeout=30
network_timeout=60
base_path=util/fastdfs/logs/meiduo    # FastDFS客户端存放日志文件的目录
tracker_server=运行tracker服务的机器ip:22122   # 运行tracker服务的机器ip:22122
log_level=info
use_connection_pool = false
connection_pool_max_idle_time = 3600
load_fdfs_parameters_from_tracker=false
use_storage_id = false
storage_ids_filename = storage_ids.conf
http.tracker_server_port=80
~~~

上传文件需要先创建fdfs_client.client.Fdfs_client的对象,并指明配置文件，如:

~~~
from fdfs_client.client import Fdfs_client
client = Fdfs_client("meiduo_mall/utils/fastdfs/client.conf")
~~~

通过创建的客户端对象执行上传文件的方法:

~~~
client.upload_by_filename(文件名)
或
client.upload_by_buffer(文件bytes数据)
~~~

如：

~~~
>>> ret = client.upload_by_filename('/Users/delron/Desktop/1.png')
getting connection
<fdfs_client.connection.Connection object at 0x1098d4cc0>
<fdfs_client.fdfs_protol.Tracker_header object at 0x1098d4908>
>>> ret
{'Group name': 'group1', 'Remote file_id': 'group1/M00/00/02/CtM3BVr-k6SACjAIAAJctR1ennA809.png', 'Status': 'Upload successed.', 'Local file name': '/Users/delron/Desktop/1.png', 'Uploaded size': '151.00KB', 'Storage IP': '10.211.55.5'}

~~~

Remote file_id 即为FastDFS保存的文件的路径，可以通过网站域名和这个路径拼接成下载路径。



### 2. 自定义Django文件存储系统

Django是自带文件存储系统的，但是默认的文件存储到本地，在本项目中，需要将文件保存到FastDFS服务器上，所以需要自定义文件存储系统。

1）需要继承自django.core.files.storage.Storage

2)  支持Django不带任何参数来实例化存储类,也就是说任何设置应该从配置django.conf.settings中获取

3)  存储类中必须实现\_open()和\_save()方法，以及任何后续使用中可能用到的其他方法。

* _open(name, mode = ‘rb’)
  被Storage.open()调用,在打开文件时被调用
* save(name, content)
  被Storage.save()调用,name是传入的文件名,content是Django接收到的文件内容,该方法需要将content文件内容保存。Django会将该方法的返回值保存到数据库中对应的文件字段,也就是说该方法应该返回要保存在数据库中的文件名信息。
* exists(name)
  如果名为name的文件在文件系统中存在,按返回True,否则返回Flase
* url(name)
  返回文件的完整访问URL
* delete(name)
  删除name文件
* listdir(path)
  列出指定路径的文件
* size(name)
  返回name文件的总大小

**注意** :并不是这些方法全部都要实现，可以省略用不到的方法

~~~python
from fdfs_client.client import Fdfs_client
from django.conf import settings
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """
    定义FastDFS客户端
    """
    def __init__(self, base_url=None, client_conf=None):
        """
        初始化对象
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        # if base_url is None:
        #     base_url = settings.FASTDFS_URL
        # self.base_url = base_url
        #
        # if client_conf is None:
        #     client_conf = settings.FASTDFS_CLIENT_CONF
        # self.client_conf = client_conf

        self.base_url = base_url or settings.FASTDFS_URL  # 技巧通过or来省去if的判断
        self.client_conf = client_conf or settings.FASTDFS_CLIENT_CONF

    def _open(self, name, mode='rb'):
        """
        存储系统打开文件存储的文件时调用此方法，因为我们自定义文件存储系统类，只是为了修改上传的目的，不需要打开，所以重写方法，什么也不做pass
        :param name: 打开文件的文件名
        :param mode: 打开文件的模式
        :return:
        """
        pass

    def _save(self, name, content):
        """
        上传文件时会调用此方法,重写此方法的目的,就是让文件上传到远程FastDFS服务器中
        :param name: 要上传的文件名
        :param content: 要上传的File对象 将来需要content.read() 文件二进制读取出并上传
        :return: 保存到数据库中的FastDFS的文件名
        """
        # 创建fastDFS客户端对象，指定fdfs客户端配置文件所在路径
        # client = Fdfs_client('/root/src/www/QmpythonBlog/util/fastdfs/client.conf')
        # client = Fdfs_client(settings.FASTDFS_CLIENT_CONF)
        client = Fdfs_client(self.client_conf)
        # 上传文件
        # client.upload_by_filename() # 如果有要上传文件的绝对路径才能使用此方法进行上传图片，并且用此方法上传的图片会有文件后缀
        # 如果要上传的是文件数据二进制数据流，可以用此方法上传文件，并且上传后没有后缀
        ret = client.upload_by_buffer(content.read())

        # 判断文件是否上传成功
        if ret.get('Status') != 'Upload successed.':
            # 返回失败
            raise Exception('Upload file failed')

        # 获取返回的文件ID
        file_id = ret.get('Remote file_id')  # 获取字典中的file_id

        return file_id

    def exists(self, name):
        """
        每次进行上传文件之前就会先调用此方法进行判断,当前要上传的文件是否已经在stroage服务器,如果在就不要上传了。
        FastDFS可以自行解决文件的重名问题，所以此处返回False，告诉Django上传的都是新文件
        :param name:   要进行判断是否上传的那个文件名
        :return: (文件已存在,不上传了) / False(文件不存在,可以上传)
        """
        return False


    def url(self, name):
        """
        当需要下载Storage服务器的文件时，就会调用此方法拼接出文件完整的下载路径
        :param name: 要下载的文件file_id
        :return: Storage服务器ip:端口 + file_id
        """
        return self.base_url + name
~~~



# python学习之美多商城(十四):商品部分:CKEditor富文本编辑器在Django中的使用、添加项目测试数据

## 一、CKEditor富文本编辑器

在运营后台，运营人员需要录入商品并编辑商品的详情信息，而商品的详情信息不是普通的文本，可以是包含了HTML语法格式的字符串。为了快速简单的让用户能够在页面中编辑带格式的文本，我们引入富文本编辑器。富文本即具备丰富样式格式的文本。

我们使用功能强大的CKEditor富文本编辑器。

![1561444038320](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561444038320.png)

### 1. 安装

~~~
pip install django-ckeditor
~~~

### 2. 添加应用

~~~python
NSTALLED_APPS = [
    ...
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
    ...
]
~~~

### 3. 添加CKEditor设置

在settings/dev.py中添加：

~~~python
# 富文本编辑器ckeditor配置

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 完整工具条
        'height': 300,  # 编辑高度
        # 'woidth': 300, # 编辑宽度
    },
}
CKEDITOR_UPLOAD_PATH = ''   # 上传图片保存路径,使用了fastDFS,设置为''
~~~

### 4. 添加ckeditor路由

在总路由中添加：

~~~python
urlpatterns = [
    ...
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
~~~

### 5. 为模型类添加字段

ckeditor提供了两种类型的Django模型类字段

- ckeditor.fields.RichTextField 不支持上传文件的富文本字段
- ckeditor_uploader.fields.RichTextUploadingField 支持上传文件的富文本字段

在商品模型类(SPU)中,需要保存商品的详细介绍、包装信息、售后服务，这三个字段需要作为富文本字段。

~~~python
class Goods(BaseModel):
    """
    商品SPU
    """
	...
	desc_detail = RichTextUploadingField(default='', verbose_name='详细介绍')
	desc_pack = RichTextField(default='', verbose_name='包装信息')
	desc_service = RichTextUploadingField(default='', verbose_name='售后服务')
	    ...
~~~

重新提交数据库：

~~~
python manage.py makemigrations
python manage.py migrate
~~~

### 6. 修改Bug

我们将通过Django上传的图片保存到了FastDFS中，而保存在FastDFS中的文件名没有后缀名，ckeditor在处理上传后的文件名按照有后缀名来处理，所以会出现bug错误。

![1561445430299](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561445430299.png)

解决办法：找到虚拟环境目录中的ckeditor_uploader/views.py文件，如

~~~
~/.virtualenvs/meiduo/lib/python3.5/site-packages/ckeditor_uploader/views.py
~~~

![1561445817418](C:\Users\44801\AppData\Roaming\Typora\typora-user-images\1561445817418.png)



## 二、将模型添加到admin

在应用的`admin.py`中注册

~~~
from django.contrib import admin
from .models import Content, ContentCategory

# Register your models here.
admin.site.register(ContentCategory)
admin.site.register(Content)

~~~

修改app显示名称：

![img](https://upload-images.jianshu.io/upload_images/9286065-9ed741481fe70d7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/333/format/webp)

所有跟app相关的内容配置，可以实现一个`Appconfig`类的子类来完成，django一般会默认在`apps.py`中建立一个。然后在apps.py对应的子类中配置verbose_name

~~~python
from django.apps import AppConfig

class ContentsConfig(AppConfig):
    name = 'contents'
    verbose_name = '广告内容'

~~~

再指定一下即可，需要管理的`__init__.py`中配置如下：

~~~python
from .apps import *
default_app_config = 'contents.apps.ContentsConfig'
~~~

添加测试数据：

~~~
# mysql -h数据库ip地址 -u数据库用户名 -p数据库密码 数据库 < sql文件
mysql -h127.0.0.1 -umeiduo -pmeiduo meiduo_mall < goods_data.sql
~~~

