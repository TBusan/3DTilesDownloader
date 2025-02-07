#http://data1.mars3d.cn/3dtiles/qx-simiao/tileset.json
#http://data1.mars3d.cn/3dtiles/qx-simiao/Data/Tile_p004_p001/Tile_p004_p001.json
#http://data1.mars3d.cn/3dtiles/qx-simiao/Data/Tile_p005_p003/Tile_p005_p003_L15_0.b3dm


1，baseUrl：http://data1.mars3d.cn/3dtiles/qx-simiao/
2，http://data1.mars3d.cn/3dtiles/qx-simiao/tileset.json是跟节点，就是放在文件夹下的tileset.json文件，不需要再次下载。
3，get请求的hear参数 origin:http://mars3d.cn/;host:data1.mars3d.cn;accept-encoding:gzip, deflate;referer:http://mars3d.cn/;
4，根据tileset.json文件，下载其他文件，有.json文件和.b3dm文件。
5，文件下载的规则，先读取tileset.json文件，找到root节点下的所有的content叶子节点中的url属性，该url属性地址就是要进行下载的文件，从该地址可以知道要下载的文件是.json文件或.b3dm文件。
6，如果content叶子节点中的url属性是.json文件，则需要下载该文件，下载的地址baseUrl加上url属性，才能得到完整的地址。
7，下载的json文件的时候需要先在本地创建文件夹，创建本地的文件夹，创建文件夹的规则是以url中的"/"分割的字符串创建文件夹，"/"分割的最后字符串是要下载的文件，将要下载的json文件放置在创建文件夹的最后一层。
8，json文件下载后，读取下载的json文件，获取json文件中的所有content叶子节点中的url属性，文件是.b3dm文件，.b3dm文件需要和baseUrl，再与当前json所在的父亲目录，再加上content中的url地址，就是要下载的b3dm的完整地址，将b3dm放置在对应的json文件所在的目录下；如果content叶子节点中的url属性是.json文件，json文件的url需要与baseUrl,再与当前json所在的父亲目录，再加上content中的url，就是要下载的json文件的完整地址，将json放置在对应的json文件所在的目录下。
9，如果步骤8中下载的是json文件，重复8的步骤，如果是b3dm文件，则不不用管。
10，根据上述规则创建一个python脚本，进行文件的下载。

