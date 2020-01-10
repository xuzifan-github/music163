import pymysql

# 建库和建表
con = pymysql.connect(
    host='localhost',
    user='root',
    passwd='A123456',
    port=50036,
    charset='utf8'
)
cur = con.cursor()
# 开始建库
cur.execute("create database 163music character set utf8;")
# 使用库
cur.execute("use 163music;")
# 建表
cur.execute('''
CREATE TABLE `comments`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `music_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL COMMENT '评论用户id',
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '昵称',
  `avatar_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '头像',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论内容',
  `comment_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论时间',
  `liked_count` int(10) NOT NULL COMMENT '点赞数',
  `content_md5` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论内容md5',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
''')

cur.execute('''
CREATE TABLE `music`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `music_id` int(10) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `cover` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '缩略图',
  `upload_author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '上传作者',
  `upload_author_avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '上传作者头像',
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `tag` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标签',
  `lyric` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '歌词',
  `entry_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据录入日期',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '数据录入状态',
  `album` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '歌曲所属的专辑',
  `artist` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '歌手',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
''')

cur.execute('''
CREATE TABLE `music_file`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `music_id` int(10) NOT NULL,
  `download_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `file_size` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `file_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
''')

# 关闭数据库连接
con.close()
